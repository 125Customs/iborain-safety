import {
  FrameType,
  PROTOCOL_VERSION,
  backoffDelayMs,
  decodeBinaryFrame,
  encodeBinaryFrame,
  parseServerMsg,
} from "@pixel-bot/protocol";
import { MicCapture, SpeakerQueue } from "./audio";
import { SentryBeacon } from "./eyes";

const $ = <T extends HTMLElement>(id: string): T => document.getElementById(id) as T;
const logEl = $("log");
function log(line: string): void {
  logEl.textContent = `${new Date().toISOString().slice(11, 19)} ${line}\n${logEl.textContent}`.slice(0, 8000);
}

const beacon = new SentryBeacon(($("face") as HTMLCanvasElement).getContext("2d")!);
beacon.sleep();

let ws: WebSocket | null = null;
let mic: MicCapture | null = null;
let speaker: SpeakerQueue | null = null;
let attempt = 0;
let wantConnected = false;

// ---- Latency HUD -----------------------------------------------------------
const rtts: number[] = [];
let lastSpeechEndedAt = 0;
let awaitingReply = false;
let turnCount = 0;
let jpegCount = 0;

function recordRtt(firstAudioAt: number): void {
  if (!awaitingReply || lastSpeechEndedAt === 0) return;
  awaitingReply = false;
  const rtt = Math.round(firstAudioAt - lastSpeechEndedAt);
  rtts.push(rtt);
  rtts.sort((a, b) => a - b);
  turnCount += 1;
  const med = rtts[Math.floor(rtts.length / 2)] ?? 0;
  const rttEl = $("rtt");
  rttEl.textContent = String(rtt);
  rttEl.classList.toggle("bad", rtt > 800);
  const medEl = $("rttMed");
  medEl.textContent = String(med);
  medEl.classList.toggle("bad", med > 800);
  $("turns").textContent = String(turnCount);
  log(`Sentry turn latency ${rtt}ms (median ${med}ms)`);
}

// ---- Camera: JPEG on vehicle / scene-change only ---------------------------
const DIFF_W = 64;
const DIFF_H = 48;
const SCENE_CHANGE_THRESHOLD = 12;
const MIN_FRAME_INTERVAL_MS = 1000;
const KEYFRAME_INTERVAL_MS = 10_000;

let prevPixels: Uint8ClampedArray | null = null;
let lastJpegAt = 0;

function startCamera(video: HTMLVideoElement): void {
  const diffCanvas = document.createElement("canvas");
  diffCanvas.width = DIFF_W;
  diffCanvas.height = DIFF_H;
  const diffCtx = diffCanvas.getContext("2d", { willReadFrequently: true })!;
  const jpegCanvas = document.createElement("canvas");
  jpegCanvas.width = 640;
  jpegCanvas.height = 480;
  const jpegCtx = jpegCanvas.getContext("2d")!;

  setInterval(() => {
    if (ws?.readyState !== WebSocket.OPEN || video.readyState < 2) return;
    const now = Date.now();
    if (now - lastJpegAt < MIN_FRAME_INTERVAL_MS) return;

    diffCtx.drawImage(video, 0, 0, DIFF_W, DIFF_H);
    const pixels = diffCtx.getImageData(0, 0, DIFF_W, DIFF_H).data;
    let changed = now - lastJpegAt > KEYFRAME_INTERVAL_MS;
    if (!changed && prevPixels) {
      let sum = 0;
      for (let i = 0; i < pixels.length; i += 4) {
        sum += Math.abs((pixels[i] ?? 0) - (prevPixels[i] ?? 0));
      }
      changed = sum / (pixels.length / 4) > SCENE_CHANGE_THRESHOLD;
    } else if (!prevPixels) {
      changed = true;
    }
    prevPixels = new Uint8ClampedArray(pixels);
    if (!changed) return;

    lastJpegAt = now;
    jpegCtx.drawImage(video, 0, 0, 640, 480);
    jpegCanvas.toBlob(
      (blob) => {
        if (!blob || ws?.readyState !== WebSocket.OPEN) return;
        void blob.arrayBuffer().then((ab) => {
          ws?.send(
            encodeBinaryFrame({ type: FrameType.Jpeg, captureTsMs: now, payload: new Uint8Array(ab) }),
          );
          jpegCount += 1;
          $("jpegs").textContent = String(jpegCount);
        });
      },
      "image/jpeg",
      0.7,
    );
  }, 250);
}

function hasSpeechEnergy(pcm16: Uint8Array): boolean {
  const view = new DataView(pcm16.buffer, pcm16.byteOffset, pcm16.byteLength);
  let sum = 0;
  const n = Math.floor(pcm16.length / 2);
  for (let i = 0; i < n; i += 4) sum += Math.abs(view.getInt16(i * 2, true));
  return sum / (n / 4) > 500;
}

function setStatus(connected: boolean, text: string): void {
  $("status").classList.toggle("on", connected);
  $("statusText").textContent = text;
}

async function connect(): Promise<void> {
  wantConnected = true;
  const base = ($("url") as HTMLInputElement).value.replace(/\/$/, "");
  const device = ($("device") as HTMLInputElement).value;
  const token = ($("token") as HTMLInputElement).value;

  speaker ??= new SpeakerQueue();
  speaker.onPlaybackStart = (ts) => {
    recordRtt(ts);
    ws?.send(JSON.stringify({ type: "playback_started", turnId: currentTurnId, ts }));
  };

  if (!mic) {
    mic = new MicCapture();
    const stream = await mic.start((pcm16, capturedAt) => {
      if (ws?.readyState !== WebSocket.OPEN) return;
      if (hasSpeechEnergy(pcm16)) {
        lastSpeechEndedAt = capturedAt;
        awaitingReply = true;
      }
      ws.send(encodeBinaryFrame({ type: FrameType.AudioIn, captureTsMs: capturedAt, payload: pcm16 }));
    });
    const video = $("cam") as HTMLVideoElement;
    video.srcObject = stream;
    void video.play();
    startCamera(video);
  }

  openSocket(base, device, token);
}

let currentTurnId = "";

function openSocket(base: string, device: string, token: string): void {
  setStatus(false, `connecting (attempt ${attempt + 1})…`);
  ws = new WebSocket(`${base}/?device=${encodeURIComponent(device)}&token=${encodeURIComponent(token)}`);
  ws.binaryType = "arraybuffer";

  ws.onopen = () => {
    attempt = 0;
    setStatus(true, "online (sentry active)");
    beacon.setState("CLEAR", "IDLE_BEACON");
    log("sentry socket connected, authenticating...");
    ws?.send(JSON.stringify({ type: "hello", proto: PROTOCOL_VERSION, deviceId: device, fw: "sentry-mock" }));
  };

  ws.onmessage = (e: MessageEvent) => {
    if (typeof e.data === "string") {
      const msg = parseServerMsg(e.data);
      if (!msg) return log(`invalid server msg: ${e.data.slice(0, 120)}`);
      switch (msg.type) {
        case "hello_ack":
          log(`sentry session ${msg.sessionId.slice(0, 8)} · daily budget ${Math.round(msg.budgetRemainingMs / 1000)}s`);
          break;
        case "control":
          currentTurnId = msg.turnId;
          beacon.setState(msg.threatLevel, msg.deterrence);

          // Update Threat Badge
          const badge = $("threatBadge");
          badge.className = `threat-badge threat-${msg.threatLevel}`;
          badge.textContent = msg.threatLevel;

          // Update Forensics UI
          if (msg.fingerprint) {
            $("fpPlate").textContent = msg.fingerprint.plate;
            $("fpType").textContent = msg.fingerprint.vehicleType.toUpperCase();
            $("fpTraits").textContent = `${msg.fingerprint.traits} ${msg.fingerprint.bodaDetails?.cargo ? `(Cargo: ${msg.fingerprint.bodaDetails.cargo})` : ""}`;
          }

          // Update Simulated WhatsApp Incident Broadcast
          const waBox = $("whatsappMsg");
          if (msg.threatLevel === "HOTLIST_MATCH" || msg.threatLevel === "EMERGENCY") {
            waBox.innerHTML = `<span style="color:#f87171;">🚨 <b>HIGH-PRIORITY THREAT ALERT:</b><br />Suspect vehicle ${msg.fingerprint?.plate ?? "UNPLATED"} flagged on Community Crime Watch. Dispatched to security patrols.</span>`;
          } else {
            waBox.innerHTML = `🛡️ <b>BomaSafety Ping:</b> ${msg.message}`;
          }

          log(`threat [${msg.threatLevel}] · deterrence [${msg.deterrence}] · ${msg.message}`);
          break;
        case "interrupted":
          speaker?.flush();
          log("scene interrupted: acoustic deterrence buffer flushed");
          break;
        case "ping":
          ws?.send(JSON.stringify({ type: "pong", ts: msg.ts }));
          break;
        case "bye":
          log(`session terminated: ${msg.reason}`);
          if (msg.reason === "session_cap") {
            setTimeout(() => openSocket(base, device, token), 50);
          }
          break;
        case "error":
          log(`sentry error ${msg.code}: ${msg.message}`);
          break;
        default:
          break;
      }
      return;
    }
    const frame = decodeBinaryFrame(new Uint8Array(e.data as ArrayBuffer));
    if (frame?.type === FrameType.AudioOut) speaker?.enqueue(frame.payload);
  };

  ws.onclose = () => {
    setStatus(false, "offline");
    beacon.sleep();
    speaker?.endTurn();
    if (wantConnected) {
      attempt += 1;
      const delay = backoffDelayMs(attempt);
      setStatus(false, `reconnecting in ${delay}ms`);
      setTimeout(() => {
        if (wantConnected) openSocket(base, device, token);
      }, delay);
    }
  };

  ws.onerror = () => log("sentry socket error");
}

$("connect").addEventListener("click", () => {
  const btn = $("connect") as HTMLButtonElement;
  if (wantConnected) {
    wantConnected = false;
    ws?.close();
    void mic?.stop();
    mic = null;
    btn.textContent = "Activate Sentry & Stream";
    btn.classList.remove("stop");
  } else {
    void connect();
    btn.textContent = "Deactivate Sentry";
    btn.classList.add("stop");
  }
});
