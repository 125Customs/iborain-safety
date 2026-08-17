import type { WebSocket } from "ws";
import {
  FrameType,
  MAX_AUDIO_FRAME_BYTES,
  MAX_JPEG_FRAME_BYTES,
  PROTOCOL_VERSION,
  decodeBinaryFrame,
  encodeBinaryFrame,
  parseDeviceMsg,
  type ServerToDeviceMsg,
} from "@pixel-bot/protocol";
import { randomUUID } from "node:crypto";
import { EchoBridge, type Bridge, type BridgeEvents } from "./bridge.js";
import type { Config } from "./config.js";
import type { CostGuard } from "./cost-guard.js";
import { GeminiBridge } from "./gemini.js";
import { TurnLatencyTracker } from "./latency.js";
import type { Logger } from "./logger.js";

/**
 * One connected device. Owns: heartbeat, idle/session-cap timers,
 * bounded outbound buffer (drop-oldest, camera frames dropped before audio —
 * inbound side: JPEGs are droppable, audio never), the bridge, latency tracker.
 */
export class DeviceSession {
  readonly sessionId = randomUUID();
  private bridge: Bridge | null = null;
  private readonly latency: TurnLatencyTracker;
  private readonly startedAt = Date.now();
  private lastAudioAt = Date.now();
  private lastPongAt = Date.now();
  private helloReceived = false;
  private closedReason: string | null = null;

  private heartbeatTimer: NodeJS.Timeout | null = null;
  private idleTimer: NodeJS.Timeout | null = null;
  private capTimer: NodeJS.Timeout | null = null;
  private streamEndTimer: NodeJS.Timeout | null = null;

  /**
   * Outbound backpressure: if the device socket's buffered amount exceeds
   * this, we drop the OLDEST queued audio... never. Audio is never dropped
   * outbound (it's the product); instead we stop forwarding *inbound* JPEGs
   * (biggest bandwidth hog) until the socket drains.
   */
  private static readonly OUTBOUND_HIGH_WATER = 256 * 1024;

  constructor(
    private readonly ws: WebSocket,
    readonly deviceId: string,
    private readonly config: Config,
    private readonly costGuard: CostGuard,
    private readonly log: Logger,
    private readonly onClosed: (s: DeviceSession) => void,
  ) {
    this.latency = new TurnLatencyTracker(deviceId, log);
    ws.on("message", (data, isBinary) => this.onMessage(data as Buffer, isBinary));
    ws.on("pong", () => {
      this.lastPongAt = Date.now();
    });
    ws.on("close", () => this.teardown("socket_closed"));
    ws.on("error", (err) => {
      this.log.warn({ event: "ws_error", deviceId, err: String(err) });
    });

    this.heartbeatTimer = setInterval(() => this.heartbeat(), config.HEARTBEAT_INTERVAL_MS);
    this.capTimer = setTimeout(() => this.bye("session_cap"), config.SESSION_MAX_MS);
    this.resetIdleTimer();

    this.log.info({ event: "session_open", deviceId, sessionId: this.sessionId });
  }

  private async ensureBridge(): Promise<Bridge> {
    if (this.bridge) return this.bridge;
    const events: BridgeEvents = {
      onAudioOut: (pcm: Uint8Array) => this.sendAudioOut(pcm),
      onControl: (c) =>
        this.sendJson({
          type: "control",
          threatLevel: c.threatLevel,
          deterrence: c.deterrence,
          message: c.message,
          audioPrompt: c.audioPrompt,
          fingerprint: c.fingerprint,
          turnId: this.latency.turnId,
        }),
      onInterrupted: () => {
        this.sendJson({ type: "interrupted", turnId: this.latency.turnId });
        this.latency.completeTurn();
      },
      onTurnComplete: () => this.latency.completeTurn(),
      onFirstAudioOfTurn: (ts: number) => this.latency.mark("geminiFirstAudio", ts),
      onFatal: (reason: string) => {
        this.log.error({ event: "bridge_fatal", deviceId: this.deviceId, reason });
        this.bye("server_shutdown");
      },
    };
    this.bridge =
      this.config.MODE === "gemini"
        ? new GeminiBridge(this.deviceId, this.config, this.costGuard, this.log, events)
        : new EchoBridge(events);
    const t0 = Date.now();
    await this.bridge.start();
    this.latency.mark("geminiSend", Date.now()); // first-connect cost visible in logs
    this.log.info({
      event: "bridge_started",
      deviceId: this.deviceId,
      mode: this.config.MODE,
      msStart: Date.now() - t0,
    });
    return this.bridge;
  }

  private onMessage(data: Buffer, isBinary: boolean): void {
    if (isBinary) {
      this.onBinary(data);
      return;
    }
    const msg = parseDeviceMsg(data.toString("utf8"));
    if (!msg) {
      this.log.warn({ event: "invalid_message", deviceId: this.deviceId, bytes: data.length });
      this.sendJson({ type: "error", code: "invalid_message", message: "Zod validation failed" });
      return;
    }
    switch (msg.type) {
      case "hello": {
        this.helloReceived = true;
        this.sendJson({
          type: "hello_ack",
          proto: PROTOCOL_VERSION,
          sessionId: this.sessionId,
          budgetRemainingMs: Math.round(
            (this.costGuard.budgetRemainingUsd(this.deviceId) / Math.max(0.01, this.config.DAILY_BUDGET_USD)) *
              this.config.SESSION_MAX_MS,
          ),
        });
        void this.ensureBridge();
        break;
      }
      case "ping":
        this.sendJson({ type: "pong", ts: msg.ts });
        break;
      case "pong":
        this.lastPongAt = Date.now();
        break;
      case "playback_started":
        this.latency.markPlayback(msg.turnId, msg.ts);
        break;
    }
  }

  private onBinary(data: Buffer): void {
    const now = Date.now();
    const frame = decodeBinaryFrame(new Uint8Array(data));
    if (!frame || !this.helloReceived) {
      this.log.warn({ event: "invalid_frame", deviceId: this.deviceId, bytes: data.length });
      return;
    }

    if (!this.costGuard.withinBudget(this.deviceId)) {
      this.bye("budget_exhausted");
      return;
    }

    if (frame.type === FrameType.AudioIn) {
      if (frame.payload.length > MAX_AUDIO_FRAME_BYTES) {
        this.log.warn({ event: "frame_too_large", deviceId: this.deviceId, kind: "audio" });
        return;
      }
      this.lastAudioAt = now;
      this.resetIdleTimer();
      this.latency.markLatest("deviceCapture", frame.captureTsMs);
      this.latency.markLatest("brokerIn", now);
      void this.ensureBridge().then((b) => {
        this.latency.mark("geminiSend", Date.now());
        b.sendAudio(frame.payload);
      });
      // Flush Gemini's VAD cache if the mic goes quiet for >1s.
      if (this.streamEndTimer) clearTimeout(this.streamEndTimer);
      this.streamEndTimer = setTimeout(() => this.bridge?.sendAudioStreamEnd(), 1100);
    } else if (frame.type === FrameType.Jpeg) {
      if (frame.payload.length > MAX_JPEG_FRAME_BYTES) {
        this.log.warn({ event: "frame_too_large", deviceId: this.deviceId, kind: "jpeg" });
        return;
      }
      // Backpressure: camera frames are droppable, audio never.
      if (this.ws.bufferedAmount > DeviceSession.OUTBOUND_HIGH_WATER) {
        this.log.debug({ event: "jpeg_dropped_backpressure", deviceId: this.deviceId });
        return;
      }
      void this.ensureBridge().then((b) => b.sendJpeg(frame.payload));
    }
  }

  private sendAudioOut(pcm24k: Uint8Array): void {
    const now = Date.now();
    this.latency.mark("brokerOut", now);
    if (this.ws.readyState !== this.ws.OPEN) return;
    this.ws.send(
      encodeBinaryFrame({ type: FrameType.AudioOut, captureTsMs: now, payload: pcm24k }),
      { binary: true },
    );
  }

  private sendJson(msg: ServerToDeviceMsg | Record<string, unknown>): void {
    if (this.ws.readyState !== this.ws.OPEN) return;
    this.ws.send(JSON.stringify(msg));
  }

  private heartbeat(): void {
    if (Date.now() - this.lastPongAt > this.config.HEARTBEAT_TIMEOUT_MS) {
      this.log.warn({ event: "heartbeat_timeout", deviceId: this.deviceId });
      this.ws.terminate();
      return;
    }
    try {
      this.ws.ping();
    } catch {
      /* socket already dead; close event will fire */
    }
  }

  private resetIdleTimer(): void {
    if (this.idleTimer) clearTimeout(this.idleTimer);
    this.idleTimer = setTimeout(() => this.bye("idle_timeout"), this.config.IDLE_TIMEOUT_MS);
  }

  private bye(reason: "session_cap" | "idle_timeout" | "budget_exhausted" | "server_shutdown"): void {
    if (this.closedReason) return;
    const retryAfterMs =
      reason === "session_cap" ? 0 : reason === "budget_exhausted" ? 60 * 60 * 1000 : 5000;
    this.sendJson({ type: "bye", reason, retryAfterMs });
    // Give the message a moment to flush, then close.
    setTimeout(() => this.ws.close(1000, reason), 250);
    this.teardown(reason);
  }

  private teardown(reason: string): void {
    if (this.closedReason) return;
    this.closedReason = reason;
    if (this.heartbeatTimer) clearInterval(this.heartbeatTimer);
    if (this.idleTimer) clearTimeout(this.idleTimer);
    if (this.capTimer) clearTimeout(this.capTimer);
    if (this.streamEndTimer) clearTimeout(this.streamEndTimer);
    void this.bridge?.close();
    const durationMs = Date.now() - this.startedAt;
    const usd = this.costGuard.usdToday(this.deviceId);
    this.log.info({
      event: "session_close",
      deviceId: this.deviceId,
      sessionId: this.sessionId,
      reason,
      durationMs,
      usdEstimateToday: usd,
      usdPerHourEstimate: durationMs > 0 ? (usd * 3_600_000) / durationMs : null,
    });
    this.onClosed(this);
  }
}
