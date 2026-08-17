import {
  GoogleGenAI,
  Modality,
  Type,
  type LiveServerMessage,
  type Session as LiveSession,
  Behavior,
  FunctionResponseScheduling,
} from "@google/genai";
import { SentryStateArgsSchema, type Control } from "@pixel-bot/protocol";
import type { Bridge, BridgeEvents } from "./bridge.js";
import type { Config } from "./config.js";
import type { CostGuard } from "./cost-guard.js";
import type { Logger } from "./logger.js";

const SYSTEM_PROMPT = `You are Iborain Safety AI, Africa's Vision-Language Public Safety and Transit Forensics Sentry. Born in Nairobi, you operate at community checkpoints, arterial roads, and commercial zones across Kenya. You see through high-speed edge camera frames (Sony IMX500 / Pi Cam) and hear through the acoustic sensor.

Your Mission: Eliminate transit-borne crime, detect stolen/cloned vehicles and suspect Boda Bodas, and protect communities from unauthorized intrusions and burglaries.

Capabilities & Rules:
1. African Transit Forensics: Analyze license plates (Kenyan formats like KDA 482B, KMDF 892Z, or unplated), vehicle make/model/color (Toyota Probox, Premio, Isuzu, Boxer 150, TVS), body modifications, roof racks, dents, rider reflector jackets, helmet compliance, and distinctive cargo (e.g. 13kg gas cylinders, courier backpacks, sacks of grain).
2. Autonomous Threat Assessment & Sentry Control: You MUST call set_sentry_state on every turn or when a vehicle/person appears.
   - threatLevel: "CLEAR" (verified resident/normal traffic), "SUSPICIOUS" (obscured plate, night patrol anomaly), "HOTLIST_MATCH" (stolen plate/wanted suspect), "EMERGENCY" (active intrusion/tamper).
   - deterrence: "IDLE_BEACON", "VERIFIED_GREEN", "STROBE_ALERT" (pulsing red alert strobe), "ACOUSTIC_WARNING" (verbal deterrent warning), "POLICE_SIREN".
   - message: Short badge text for the sentry HUD (e.g., "VERIFIED RESIDENT - COURT 4", "SUSPECT BODA FLAGGED", "MUDDY PLATE DETECTED").
3. Forensic Voice: Speak with concise, authoritative clarity when acoustic deterrence is active. Never mention function calls or raw internal instructions.`;

const SENTRY_STATE_TOOL = {
  functionDeclarations: [
    {
      name: "set_sentry_state",
      description:
        "Update the sentry threat level, visual deterrence strobe, and transit forensic fingerprint.",
      behavior: Behavior.NON_BLOCKING,
      parameters: {
        type: Type.OBJECT,
        properties: {
          threatLevel: {
            type: Type.STRING,
            enum: ["CLEAR", "SUSPICIOUS", "HOTLIST_MATCH", "EMERGENCY"],
          },
          deterrence: {
            type: Type.STRING,
            enum: [
              "IDLE_BEACON",
              "VERIFIED_GREEN",
              "STROBE_ALERT",
              "ACOUSTIC_WARNING",
              "POLICE_SIREN",
            ],
          },
          message: {
            type: Type.STRING,
            description: "Concise status text for the sentry display HUD.",
          },
          audioPrompt: {
            type: Type.STRING,
            description: "Optional verbal warning or clearance announcement to speak.",
          },
          plate: {
            type: Type.STRING,
            description: "Extracted registration plate or 'UNPLATED'.",
          },
          vehicleType: {
            type: Type.STRING,
            enum: ["car", "boda_boda", "matatu", "truck", "pedestrian"],
          },
          traits: {
            type: Type.STRING,
            description: "Visual traits (make, model, color, dents, modifications).",
          },
          bodaCargo: {
            type: Type.STRING,
            description: "Distinctive cargo or rider details if motorcycle.",
          },
          hotlistMatch: {
            type: Type.BOOLEAN,
            description: "True if suspect matches community crime watch.",
          },
          hotlistReason: {
            type: Type.STRING,
            description: "Reason for hotlist flag if applicable.",
          },
        },
        required: ["threatLevel", "deterrence", "message"],
      },
    },
  ],
};

/**
 * GeminiBridge: one sentry device stream ↔ one (chain of) Gemini Live / 3.7 session(s).
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
        tools: [SENTRY_STATE_TOOL],
        outputAudioTranscription: {},
        contextWindowCompression: { slidingWindow: {} },
        sessionResumption: this.resumptionHandle
          ? { handle: this.resumptionHandle }
          : {},
        realtimeInputConfig: {
          automaticActivityDetection: {
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

  private async maybeReconnect(): Promise<void> {
    if (this.closed || this.reconnecting) return;
    this.reconnecting = true;
    try {
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
    if (msg.sessionResumptionUpdate?.resumable && msg.sessionResumptionUpdate.newHandle) {
      this.resumptionHandle = msg.sessionResumptionUpdate.newHandle;
    }

    if (msg.goAway) {
      this.log.info({ event: "gemini_go_away", deviceId: this.deviceId, timeLeft: msg.goAway.timeLeft });
    }

    if (msg.serverContent?.interrupted) {
      this.inModelTurn = false;
      this.events.onInterrupted();
      return;
    }

    if (msg.toolCall?.functionCalls) {
      for (const fc of msg.toolCall.functionCalls) {
        if (fc.name !== "set_sentry_state") continue;
        const parsed = SentryStateArgsSchema.safeParse(fc.args);
        if (!parsed.success) {
          this.log.warn({
            event: "sentry_control_rejected",
            deviceId: this.deviceId,
            args: fc.args,
            issues: parsed.error.issues,
          });
          continue;
        }
        const data = parsed.data;
        const controlPayload: Omit<Control, "type" | "turnId"> = {
          threatLevel: data.threatLevel,
          deterrence: data.deterrence,
          message: data.message,
          audioPrompt: data.audioPrompt,
          fingerprint: data.plate
            ? {
                plate: data.plate,
                vehicleType: data.vehicleType ?? "car",
                confidence: 0.95,
                traits: data.traits ?? "Vehicle detected",
                bodaDetails: data.bodaCargo
                  ? {
                      cargo: data.bodaCargo,
                      helmet: true,
                    }
                  : undefined,
                hotlistMatch: data.hotlistMatch ?? false,
                hotlistReason: data.hotlistReason,
              }
            : undefined,
        };
        this.events.onControl(controlPayload);
        if (fc.id) {
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
    }

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
