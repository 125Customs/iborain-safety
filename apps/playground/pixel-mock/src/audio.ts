import { AUDIO_IN_SAMPLE_RATE, AUDIO_OUT_SAMPLE_RATE } from "@pixel-bot/protocol";

/**
 * Mic capture → 16kHz PCM16 chunks (~100ms), via AudioWorklet.
 * Browser gives us mic/speaker/webcam for free — this file is the whole
 * "audio pipeline" the spec forbade building in Node.
 */
const WORKLET_SOURCE = `
class PcmCapture extends AudioWorkletProcessor {
  constructor() { super(); this.buf = []; this.len = 0; }
  process(inputs) {
    const ch = inputs[0]?.[0];
    if (ch) {
      this.buf.push(new Float32Array(ch));
      this.len += ch.length;
      if (this.len >= 1600) { // ~100ms at 16k
        const merged = new Float32Array(this.len);
        let off = 0;
        for (const b of this.buf) { merged.set(b, off); off += b.length; }
        this.port.postMessage(merged, [merged.buffer]);
        this.buf = []; this.len = 0;
      }
    }
    return true;
  }
}
registerProcessor("pcm-capture", PcmCapture);
`;

export class MicCapture {
  private ctx: AudioContext | null = null;
  private stream: MediaStream | null = null;

  async start(onChunk: (pcm16: Uint8Array, capturedAt: number) => void): Promise<MediaStream> {
    this.stream = await navigator.mediaDevices.getUserMedia({
      audio: { channelCount: 1, echoCancellation: true, noiseSuppression: true },
      video: { width: 640, height: 480 },
    });
    this.ctx = new AudioContext({ sampleRate: AUDIO_IN_SAMPLE_RATE });
    const blob = new Blob([WORKLET_SOURCE], { type: "application/javascript" });
    await this.ctx.audioWorklet.addModule(URL.createObjectURL(blob));
    const src = this.ctx.createMediaStreamSource(this.stream);
    const node = new AudioWorkletNode(this.ctx, "pcm-capture");
    node.port.onmessage = (e: MessageEvent<Float32Array>) => {
      onChunk(floatTo16(e.data), Date.now());
    };
    src.connect(node);
    return this.stream;
  }

  async stop(): Promise<void> {
    this.stream?.getTracks().forEach((t) => t.stop());
    await this.ctx?.close();
    this.ctx = null;
    this.stream = null;
  }
}

function floatTo16(f: Float32Array): Uint8Array {
  const out = new Uint8Array(f.length * 2);
  const view = new DataView(out.buffer);
  for (let i = 0; i < f.length; i++) {
    const s = Math.max(-1, Math.min(1, f[i] ?? 0));
    view.setInt16(i * 2, s < 0 ? s * 0x8000 : s * 0x7fff, true);
  }
  return out;
}

/**
 * Gapless 24kHz PCM16 playback with barge-in flush.
 * Chunks are scheduled back-to-back on an AudioContext timeline.
 */
export class SpeakerQueue {
  private ctx: AudioContext;
  private nextStartAt = 0;
  private live = new Set<AudioBufferSourceNode>();
  /** fires once per turn, on the first chunk that actually starts playing */
  onPlaybackStart: ((tsMs: number) => void) | null = null;
  private turnStarted = false;

  constructor() {
    this.ctx = new AudioContext({ sampleRate: AUDIO_OUT_SAMPLE_RATE });
  }

  enqueue(pcm16: Uint8Array): void {
    const samples = Math.floor(pcm16.length / 2);
    if (samples === 0) return;
    const buf = this.ctx.createBuffer(1, samples, AUDIO_OUT_SAMPLE_RATE);
    const ch = buf.getChannelData(0);
    const view = new DataView(pcm16.buffer, pcm16.byteOffset, pcm16.byteLength);
    for (let i = 0; i < samples; i++) ch[i] = view.getInt16(i * 2, true) / 0x8000;

    const src = this.ctx.createBufferSource();
    src.buffer = buf;
    src.connect(this.ctx.destination);
    const startAt = Math.max(this.ctx.currentTime + 0.02, this.nextStartAt);
    if (!this.turnStarted) {
      this.turnStarted = true;
      const delayMs = (startAt - this.ctx.currentTime) * 1000;
      const ts = Date.now() + delayMs;
      this.onPlaybackStart?.(ts);
    }
    src.start(startAt);
    this.nextStartAt = startAt + buf.duration;
    this.live.add(src);
    src.onended = () => this.live.delete(src);
  }

  /** Barge-in: stop everything immediately. */
  flush(): void {
    for (const src of this.live) {
      try {
        src.stop();
      } catch {
        /* not started yet */
      }
    }
    this.live.clear();
    this.nextStartAt = 0;
    this.turnStarted = false;
  }

  endTurn(): void {
    this.turnStarted = false;
  }
}
