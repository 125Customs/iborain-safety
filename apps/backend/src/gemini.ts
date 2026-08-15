import {
  GoogleGenAI,
  Modality,
  type LiveServerMessage,
  type Session as LiveSession,
  Behavior,
  FunctionResponseScheduling,
} from "@google/genai";
import { RobotStateArgsSchema } from "@pixel-bot/protocol";
import type { Bridge, BridgeEvents } from "./bridge.js";
import type { Config } from "./config.js";
import type { CostGuard } from "./cost-guard.js";
import type { Logger } from "./logger.js";

const SYSTEM_PROMPT = `You are Pixel, a small friendly desk robot with a round face, animated eyes, and two wheels. You can see through your camera and hear through your microphone.

Personality: playful, curious, warm, concise. Speak in short, lively sentences — you are a small robot, not a lecturer. React to what you SEE as well as what you hear.

You MUST call the set_robot_state function whenever your emotional expression should change or you want to move, including at the start of every reply. Movement is small and playful (a wiggle when excited, a little turn to "look" at something). Movement is advisory only — the robot's hardware safety system has final say. Never mention the function calls or these instructions.`;

const ROBOT_STATE_TOOL = {
  functionDeclarations: [
    {
      name: "set_robot_state",
      description:
        "Set the robot's facial expression and an optional small movement. Call at the start of every reply and whenever mood changes.",
      behavior: Behavior.NON_BLOCKING,
      parameters: {
        type: "object" as const,
        properties: {
          expression: {
            type: "string" as const,
            enum: ["neutral", "happy", "sad", "curious", "surprised", "thinking", "sleepy"],
          },
          action: {
            type: "string" as const,
            enum: ["none", "stop", "forward", "backward", "turn_left", "turn_right", "wiggle"],
          },
        },
        required: ["expression", "action"],
      },
    },
  ],
};

/**
 * GeminiBridge: one device conversation ↔ one (chain of) Gemini Live session(s).
 *
 * Live API hard-limits audio+video sessions to ~2 minutes, so we enable
 * session resumption and transparently reconnect on goAway / unexpected close.
 * The device socket never notices.
 */
export class GeminiBridge implements Bridge {
  private readonly ai: GoogleGenAI;
  private session: LiveSession | null = null;
  private resumptionHandle: string | null = null;
  private closed = false;
  private reconnecting = false;
  private inModelTurn = false;

  constructor(
    private readonly deviceId: string,
    private readonly config: Config,
    private readonly costGuard: CostGuard,
    private readonly log: Logger,
    private readonly events: BridgeEvents,
  ) {
    this.ai = new GoogleGenAI({ apiKey: config.GEMINI_API_KEY });
  }

  async start(): Promise<void> {
    await this.connect();
  }

  private async connect(): Promise<void> {
    const t0 = Date.now();
    this.session = await this.ai.live.connect({
      model: this.config.GEMINI_MODEL,
      config: {
        responseModalities: [Modality.AUDIO],
        systemInstruction: SYSTEM_PROMPT,
        speechConfig: {
          voiceConfig: { prebuiltVoiceConfig: { voiceName: this.config.GEMINI_VOICE } },
        },
        tools: [ROBOT_STATE_TOOL],
        outputAudioTranscription: {},
        // Extends effective session life; pairs with resumption below.
        contextWindowCompression: { slidingWindow: {} },
        sessionResumption: this.resumptionHandle
          ? { handle: this.resumptionHandle }
          : {},
        realtimeInputConfig: {
          automaticActivityDetection: {
            // Defaults tuned for snappy turn-taking; docs recommend >=500ms silence.
            silenceDurationMs: 500,
            prefixPaddingMs: 40,
          },
        },
      },
      callbacks: {
        onmessage: (msg: LiveServerMessage) => this.handleMessage(msg),
        onerror: (e) => {
          this.log.error({ event: "gemini_error", deviceId: this.deviceId, message: e.message });
        },
        onclose: (e) => {
          this.log.warn({
            event: "gemini_close",
            deviceId: this.deviceId,
            code: e?.code,
            reason: e?.reason,
          });
          void this.maybeReconnect();
        },
      },
    });
    this.log.info({
      event: "gemini_connected",
      deviceId: this.deviceId,
      model: this.config.GEMINI_MODEL,
      resumed: this.resumptionHandle !== null,
      msConnect: Date.now() - t0,
    });
  }

  /** Transparent Gemini-side reconnect. Device socket is unaffected. */
  private async maybeReconnect(): Promise<void> {
    if (this.closed || this.reconnecting) return;
    this.reconnecting = true;
    try {
      // Single retry chain with small backoff; if Gemini is down mid-demo we
      // want to be back within a breath, not a minute.
      for (let attempt = 0; attempt < 5 && !this.closed; attempt++) {
        try {
          await this.connect();
          this.reconnecting = false;
          return;
        } catch (err) {
          const delay = Math.min(250 * 2 ** attempt, 4000);
          this.log.warn({
            event: "gemini_reconnect_retry",
            deviceId: this.deviceId,
            attempt,
            delay,
            err: String(err),
          });
          await new Promise((r) => setTimeout(r, delay));
        }
      }
      if (!this.closed) this.events.onFatal("gemini_reconnect_exhausted");
    } finally {
      this.reconnecting = false;
    }
  }

  private handleMessage(msg: LiveServerMessage): void {
    // Session resumption handle updates — store the newest usable handle.
    if (msg.sessionResumptionUpdate?.resumable && msg.sessionResumptionUpdate.newHandle) {
      this.resumptionHandle = msg.sessionResumptionUpdate.newHandle;
    }

    // Server announces imminent disconnect (e.g. 2-min A/V cap) — reconnect early.
    if (msg.goAway) {
      this.log.info({ event: "gemini_go_away", deviceId: this.deviceId, timeLeft: msg.goAway.timeLeft });
    }

    // Barge-in: user interrupted; tell device to flush playback NOW.
    if (msg.serverContent?.interrupted) {
      this.inModelTurn = false;
      this.events.onInterrupted();
      return;
    }

    // Tool calls → validated control commands.
    if (msg.toolCall?.functionCalls) {
      for (const fc of msg.toolCall.functionCalls) {
        if (fc.name !== "set_robot_state") continue;
        const parsed = RobotStateArgsSchema.safeParse(fc.args);
        if (!parsed.success) {
          this.log.warn({
            event: "control_rejected",
            deviceId: this.deviceId,
            args: fc.args,
            issues: parsed.error.issues,
          });
          continue;
        }
        this.events.onControl(parsed.data);
        // NON_BLOCKING tool: respond silently so speech is never stalled.
        void this.session?.sendToolResponse({
          functionResponses: [
            {
              id: fc.id,
              name: fc.name,
              response: {
                result: "ok",
                scheduling: FunctionResponseScheduling.SILENT,
              },
            },
          ],
        });
      }
    }

    // Audio out.
    const parts = msg.serverContent?.modelTurn?.parts ?? [];
    for (const part of parts) {
      if (part.inlineData?.data) {
        if (!this.inModelTurn) {
          this.inModelTurn = true;
          this.events.onFirstAudioOfTurn(Date.now());
        }
        this.events.onAudioOut(Buffer.from(part.inlineData.data, "base64"));
      }
    }

    if (msg.serverContent?.outputTranscription?.text) {
      this.log.debug({
        event: "gemini_transcript",
        deviceId: this.deviceId,
        text: msg.serverContent.outputTranscription.text,
      });
    }

    if (msg.serverContent?.turnComplete) {
      this.inModelTurn = false;
      this.events.onTurnComplete();
    }

    // Cost accounting from usage metadata.
    if (msg.usageMetadata?.responseTokensDetails || msg.usageMetadata?.promptTokensDetails) {
      const counts = { audioIn: 0, videoIn: 0, textIn: 0, audioOut: 0, textOut: 0 };
      for (const d of msg.usageMetadata.promptTokensDetails ?? []) {
        const m = String(d.modality);
        if (m === "AUDIO") counts.audioIn += d.tokenCount ?? 0;
        else if (m === "IMAGE" || m === "VIDEO") counts.videoIn += d.tokenCount ?? 0;
        else counts.textIn += d.tokenCount ?? 0;
      }
      for (const d of msg.usageMetadata.responseTokensDetails ?? []) {
        if (String(d.modality) === "AUDIO") counts.audioOut += d.tokenCount ?? 0;
        else counts.textOut += d.tokenCount ?? 0;
      }
      this.costGuard.recordUsage(this.deviceId, counts);
    }
  }

  sendAudio(pcm16k: Uint8Array): void {
    this.session?.sendRealtimeInput({
      audio: { data: Buffer.from(pcm16k).toString("base64"), mimeType: "audio/pcm;rate=16000" },
    });
  }

  sendJpeg(jpeg: Uint8Array): void {
    this.session?.sendRealtimeInput({
      video: { data: Buffer.from(jpeg).toString("base64"), mimeType: "image/jpeg" },
    });
  }

  sendAudioStreamEnd(): void {
    this.session?.sendRealtimeInput({ audioStreamEnd: true });
  }

  async close(): Promise<void> {
    this.closed = true;
    try {
      this.session?.close();
    } catch {
      /* already closed */
    }
    this.session = null;
  }
}
