/**
 * 30-minute unattended soak test with fault injection.
 * Simulates a device: streams synthetic speech-shaped PCM, sends JPEGs,
 * randomly KILLS the socket (Wi-Fi drop) and reconnects with backoff+jitter.
 * Exits 0 only if the whole run needed zero manual intervention.
 *
 * Usage: SOAK_URL=ws://localhost:8080 SOAK_DEVICE=dev-local SOAK_TOKEN=local-secret pnpm soak
 *        SOAK_MINUTES=30 (default) — use 2 for a smoke run.
 */
import WebSocket from "ws";
import {
  FrameType,
  PROTOCOL_VERSION,
  backoffDelayMs,
  decodeBinaryFrame,
  encodeBinaryFrame,
} from "@pixel-bot/protocol";

const URL_BASE = process.env["SOAK_URL"] ?? "ws://localhost:8080";
const DEVICE = process.env["SOAK_DEVICE"] ?? "dev-local";
const TOKEN = process.env["SOAK_TOKEN"] ?? "local-secret";
const MINUTES = Number(process.env["SOAK_MINUTES"] ?? "30");

const stats = {
  connects: 0,
  injectedKills: 0,
  audioFramesSent: 0,
  audioFramesReceived: 0,
  jpegsSent: 0,
  errors: 0,
  latencies: [] as number[],
};

function syntheticPcm(ms: number): Uint8Array {
  const samples = Math.floor((16_000 * ms) / 1000);
  const out = new Uint8Array(samples * 2);
  const view = new DataView(out.buffer);
  for (let i = 0; i < samples; i++) {
    // Speech-ish: 200Hz fundamental + noise burst envelope
    const t = i / 16_000;
    const env = Math.abs(Math.sin(t * 3));
    const v = (Math.sin(2 * Math.PI * 200 * t) * 0.5 + (Math.random() - 0.5) * 0.2) * env;
    view.setInt16(i * 2, Math.max(-32768, Math.min(32767, Math.round(v * 20000))), true);
  }
  return out;
}

const FAKE_JPEG = new Uint8Array([0xff, 0xd8, 0xff, 0xe0, ...new Array(512).fill(0), 0xff, 0xd9]);

let attempt = 0;
let ws: WebSocket | null = null;
let stopping = false;

function connect(): void {
  if (stopping) return;
  const url = `${URL_BASE}/?device=${DEVICE}&token=${TOKEN}`;
  ws = new WebSocket(url);
  const sentAt = new Map<number, number>();

  ws.on("open", () => {
    attempt = 0;
    stats.connects += 1;
    ws?.send(JSON.stringify({ type: "hello", proto: PROTOCOL_VERSION, deviceId: DEVICE, fw: "soak" }));
  });

  ws.on("message", (data, isBinary) => {
    if (!isBinary) return;
    const frame = decodeBinaryFrame(new Uint8Array(data as Buffer));
    if (frame?.type === FrameType.AudioOut) {
      stats.audioFramesReceived += 1;
      const rtt = Date.now() - (sentAt.get(0) ?? Date.now());
      stats.latencies.push(rtt);
    }
  });

  ws.on("close", () => {
    if (stopping) return;
    attempt += 1;
    setTimeout(connect, backoffDelayMs(attempt));
  });

  ws.on("error", () => {
    stats.errors += 1;
  });

  // Talk in 2s bursts every ~6s while connected.
  const talker = setInterval(() => {
    if (ws?.readyState !== WebSocket.OPEN) return;
    sentAt.set(0, Date.now());
    const pcm = syntheticPcm(2000);
    // stream in 100ms chunks like the real device
    for (let off = 0; off < pcm.length; off += 3200) {
      ws.send(
        encodeBinaryFrame({
          type: FrameType.AudioIn,
          captureTsMs: Date.now(),
          payload: pcm.subarray(off, Math.min(off + 3200, pcm.length)),
        }),
        { binary: true },
      );
      stats.audioFramesSent += 1;
    }
    if (Math.random() < 0.3) {
      ws.send(
        encodeBinaryFrame({ type: FrameType.Jpeg, captureTsMs: Date.now(), payload: FAKE_JPEG }),
        { binary: true },
      );
      stats.jpegsSent += 1;
    }
  }, 6000);

  ws.on("close", () => clearInterval(talker));
}

// Fault injection: kill the socket at random intervals (8–40s).
function scheduleKill(): void {
  if (stopping) return;
  setTimeout(() => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      stats.injectedKills += 1;
      // eslint-disable-next-line no-console
      console.log(`[soak] 💀 injecting socket kill #${stats.injectedKills}`);
      ws.terminate();
    }
    scheduleKill();
  }, 8000 + Math.random() * 32_000);
}

connect();
scheduleKill();

setTimeout(() => {
  stopping = true;
  ws?.close();
  const sorted = [...stats.latencies].sort((a, b) => a - b);
  const p50 = sorted[Math.floor(sorted.length / 2)] ?? null;
  const p95 = sorted[Math.floor(sorted.length * 0.95)] ?? null;
  // eslint-disable-next-line no-console
  console.log("[soak] RESULT", JSON.stringify({ ...stats, latencies: undefined, p50, p95 }, null, 2));
  const ok = stats.connects >= stats.injectedKills && stats.audioFramesReceived > 0;
  // eslint-disable-next-line no-console
  console.log(ok ? "[soak] PASS — survived unattended" : "[soak] FAIL");
  process.exit(ok ? 0 : 1);
}, MINUTES * 60 * 1000);
