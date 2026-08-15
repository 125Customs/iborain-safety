import type { Logger } from "./logger.js";

/**
 * Per-turn latency breakdown. <800ms perceived round-trip IS the product,
 * so every hop gets a timestamp and every turn gets one structured log line.
 *
 * Hops:
 *  deviceCapture  — device epoch ms from the binary frame header (last audio frame of the utterance)
 *  brokerIn       — broker received that frame
 *  geminiSend     — broker forwarded to Gemini
 *  geminiFirstAudio — first audio chunk of the model turn arrived
 *  brokerOut      — first audio chunk sent to device
 *  devicePlayback — device reported playback_started (optional; device clock)
 */
export interface TurnTimestamps {
  turnId: string;
  deviceCapture?: number;
  brokerIn?: number;
  geminiSend?: number;
  geminiFirstAudio?: number;
  brokerOut?: number;
  devicePlayback?: number;
}

export class TurnLatencyTracker {
  private current: TurnTimestamps;
  private seq = 0;

  constructor(
    private readonly deviceId: string,
    private readonly log: Logger,
  ) {
    this.current = { turnId: this.nextId() };
  }

  private nextId(): string {
    this.seq += 1;
    return `${this.deviceId}-t${this.seq}`;
  }

  get turnId(): string {
    return this.current.turnId;
  }

  mark(hop: Exclude<keyof TurnTimestamps, "turnId">, ts: number): void {
    // Only the first occurrence per turn matters (first audio chunk, etc.)
    if (this.current[hop] === undefined) this.current[hop] = ts;
  }

  /** Always update: the utterance's LAST inbound audio frame is the anchor. */
  markLatest(hop: "deviceCapture" | "brokerIn", ts: number): void {
    this.current[hop] = ts;
  }

  markPlayback(turnId: string, ts: number): void {
    if (turnId === this.current.turnId) this.current.devicePlayback = ts;
  }

  /** Close out the turn, emit one structured line, start the next. */
  completeTurn(): void {
    const t = this.current;
    if (t.brokerIn !== undefined && t.brokerOut !== undefined) {
      this.log.info({
        event: "turn_latency",
        deviceId: this.deviceId,
        turnId: t.turnId,
        msBrokerToGemini:
          t.geminiSend !== undefined && t.brokerIn !== undefined ? t.geminiSend - t.brokerIn : null,
        msGeminiThinking:
          t.geminiFirstAudio !== undefined && t.geminiSend !== undefined
            ? t.geminiFirstAudio - t.geminiSend
            : null,
        msGeminiToDevice:
          t.brokerOut !== undefined && t.geminiFirstAudio !== undefined
            ? t.brokerOut - t.geminiFirstAudio
            : null,
        msBrokerRoundTrip: t.brokerOut - t.brokerIn,
        msPerceived:
          t.devicePlayback !== undefined && t.deviceCapture !== undefined
            ? t.devicePlayback - t.deviceCapture
            : null,
      });
    }
    this.current = { turnId: this.nextId() };
  }
}
