import type { Control } from "@pixel-bot/protocol";

/**
 * A Bridge is whatever sits between the device socket and "the brain".
 * EchoBridge = Phase 1 walking skeleton. GeminiBridge = Phase 2+.
 */
export interface BridgeEvents {
  /** 24kHz PCM16 mono audio for the device speaker */
  onAudioOut: (pcm: Uint8Array) => void;
  /** validated robot control command */
  onControl: (control: Omit<Control, "type" | "turnId">) => void;
  /** user barge-in: device must flush playback */
  onInterrupted: () => void;
  /** model finished its turn */
  onTurnComplete: () => void;
  /** first audio chunk of a model turn (latency hop) */
  onFirstAudioOfTurn: (tsMs: number) => void;
  /** unrecoverable bridge failure — session should close gracefully */
  onFatal: (reason: string) => void;
}

export interface Bridge {
  start(): Promise<void>;
  sendAudio(pcm16k: Uint8Array): void;
  sendJpeg(jpeg: Uint8Array): void;
  /** signal a >1s pause in the mic stream (flushes Gemini VAD cache) */
  sendAudioStreamEnd(): void;
  close(): Promise<void>;
}

/**
 * Phase 1 echo bridge: batches inbound audio and echoes it back after the
 * caller stops talking for ECHO_SILENCE_MS. Upsamples 16k → 24k (nearest
 * neighbor) so the device playback path is exercised at the real output rate.
 */
export class EchoBridge implements Bridge {
  private buffered: Uint8Array[] = [];
  private flushTimer: NodeJS.Timeout | null = null;
  private static readonly ECHO_SILENCE_MS = 500;

  constructor(private readonly events: BridgeEvents) {}

  async start(): Promise<void> {
    /* nothing to do */
  }

  sendAudio(pcm16k: Uint8Array): void {
    this.buffered.push(pcm16k);
    if (this.flushTimer) clearTimeout(this.flushTimer);
    this.flushTimer = setTimeout(() => this.flush(), EchoBridge.ECHO_SILENCE_MS);
  }

  sendJpeg(_jpeg: Uint8Array): void {
    /* echo mode ignores vision */
  }

  sendAudioStreamEnd(): void {
    this.flush();
  }

  private flush(): void {
    if (this.buffered.length === 0) return;
    const chunks = this.buffered;
    this.buffered = [];
    this.events.onFirstAudioOfTurn(Date.now());
    this.events.onControl({ expression: "happy", action: "none" });
    for (const chunk of chunks) {
      this.events.onAudioOut(upsample16to24(chunk));
    }
    this.events.onTurnComplete();
  }

  async close(): Promise<void> {
    if (this.flushTimer) clearTimeout(this.flushTimer);
  }
}

/** 16k → 24k PCM16: for every 2 input samples emit 3 (duplicate the first). */
export function upsample16to24(pcm16k: Uint8Array): Uint8Array {
  const inSamples = Math.floor(pcm16k.length / 2);
  const pairs = Math.floor(inSamples / 2);
  const out = new Uint8Array(pairs * 6);
  const inView = new DataView(pcm16k.buffer, pcm16k.byteOffset, pcm16k.byteLength);
  const outView = new DataView(out.buffer);
  for (let i = 0; i < pairs; i++) {
    const s0 = inView.getInt16(i * 4, true);
    const s1 = inView.getInt16(i * 4 + 2, true);
    outView.setInt16(i * 6, s0, true);
    outView.setInt16(i * 6 + 2, s0, true);
    outView.setInt16(i * 6 + 4, s1, true);
  }
  return out;
}
