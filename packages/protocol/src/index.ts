/**
 * @pixel-bot/protocol — FROZEN wire protocol v1.
 * Firmware implements against PROTOCOL.md, which is generated from this file's
 * definitions. Any change here bumps PROTOCOL_VERSION and PROTOCOL.md together.
 */
import { z } from "zod";

export const PROTOCOL_VERSION = 1;

// ---------------------------------------------------------------------------
// Binary frames (WebSocket binary messages)
// Layout: [1 byte frameType][8 bytes uint64 LE captureTimestampMs][payload]
// ---------------------------------------------------------------------------

export const BINARY_HEADER_BYTES = 9;

export enum FrameType {
  /** device→server: raw PCM16 mono 16kHz little-endian */
  AudioIn = 0x01,
  /** device→server: JPEG camera frame */
  Jpeg = 0x02,
  /** server→device: raw PCM16 mono 24kHz little-endian (Gemini native output rate) */
  AudioOut = 0x11,
}

export const AUDIO_IN_SAMPLE_RATE = 16_000;
export const AUDIO_OUT_SAMPLE_RATE = 24_000;
export const AUDIO_BITS = 16;
export const AUDIO_CHANNELS = 1;

/** Hard size limits — frames exceeding these are dropped and logged. */
export const MAX_AUDIO_FRAME_BYTES = 32 * 1024; // ~1s of 16k PCM16
export const MAX_JPEG_FRAME_BYTES = 300 * 1024;
export const MAX_TEXT_MESSAGE_BYTES = 4 * 1024;

export interface BinaryFrame {
  type: FrameType;
  /** device epoch ms at capture time (or server epoch for AudioOut) */
  captureTsMs: number;
  payload: Uint8Array;
}

export function encodeBinaryFrame(frame: BinaryFrame): Uint8Array {
  const out = new Uint8Array(BINARY_HEADER_BYTES + frame.payload.length);
  const view = new DataView(out.buffer);
  view.setUint8(0, frame.type);
  view.setBigUint64(1, BigInt(Math.floor(frame.captureTsMs)), true);
  out.set(frame.payload, BINARY_HEADER_BYTES);
  return out;
}

export function decodeBinaryFrame(data: Uint8Array): BinaryFrame | null {
  if (data.length < BINARY_HEADER_BYTES) return null;
  const view = new DataView(data.buffer, data.byteOffset, data.byteLength);
  const type = view.getUint8(0);
  if (
    type !== FrameType.AudioIn &&
    type !== FrameType.Jpeg &&
    type !== FrameType.AudioOut
  ) {
    return null;
  }
  return {
    type: type as FrameType,
    captureTsMs: Number(view.getBigUint64(1, true)),
    payload: data.subarray(BINARY_HEADER_BYTES),
  };
}

// ---------------------------------------------------------------------------
// Control plane (WebSocket text messages, JSON, Zod-validated on BOTH ends)
// ---------------------------------------------------------------------------

export const ExpressionSchema = z.enum([
  "neutral",
  "happy",
  "sad",
  "curious",
  "surprised",
  "thinking",
  "sleepy",
]);
export type Expression = z.infer<typeof ExpressionSchema>;

export const ActionSchema = z.enum([
  "none",
  "stop",
  "forward",
  "backward",
  "turn_left",
  "turn_right",
  "wiggle",
]);
export type Action = z.infer<typeof ActionSchema>;

/** device→server, first message after socket open */
export const HelloSchema = z.object({
  type: z.literal("hello"),
  proto: z.literal(PROTOCOL_VERSION),
  deviceId: z.string().min(1).max(64),
  /** firmware version string, free-form */
  fw: z.string().max(32).optional(),
});

/** server→device */
export const HelloAckSchema = z.object({
  type: z.literal("hello_ack"),
  proto: z.literal(PROTOCOL_VERSION),
  sessionId: z.string(),
  /** ms of session budget remaining today (cost cap awareness) */
  budgetRemainingMs: z.number().int().nonnegative(),
});

/** server→device: robot control command (from validated Gemini tool call) */
export const ControlSchema = z.object({
  type: z.literal("control"),
  expression: ExpressionSchema,
  action: ActionSchema,
  turnId: z.string(),
});
export type Control = z.infer<typeof ControlSchema>;

/**
 * server→device: barge-in — user interrupted the robot. Device must
 * immediately flush its audio playback buffer and stop the speaker.
 */
export const InterruptedSchema = z.object({
  type: z.literal("interrupted"),
  turnId: z.string(),
});

/** either direction: application-level heartbeat (in addition to WS ping/pong) */
export const PingSchema = z.object({
  type: z.literal("ping"),
  ts: z.number(),
});
export const PongSchema = z.object({
  type: z.literal("pong"),
  ts: z.number(),
});

/** device→server: playback started for a turn — closes the latency loop */
export const PlaybackStartedSchema = z.object({
  type: z.literal("playback_started"),
  turnId: z.string(),
  ts: z.number(),
});

/** server→device: server is closing the session; reason is machine-readable */
export const ByeSchema = z.object({
  type: z.literal("bye"),
  reason: z.enum([
    "session_cap",
    "idle_timeout",
    "budget_exhausted",
    "server_shutdown",
    "auth_revoked",
    "protocol_error",
  ]),
  /** device may reconnect after this many ms (0 = immediately) */
  retryAfterMs: z.number().int().nonnegative(),
});

/** server→device: non-fatal error notice */
export const ErrorMsgSchema = z.object({
  type: z.literal("error"),
  code: z.string(),
  message: z.string().max(256),
});

export const DeviceToServerMsgSchema = z.discriminatedUnion("type", [
  HelloSchema,
  PingSchema,
  PongSchema,
  PlaybackStartedSchema,
]);
export type DeviceToServerMsg = z.infer<typeof DeviceToServerMsgSchema>;

export const ServerToDeviceMsgSchema = z.discriminatedUnion("type", [
  HelloAckSchema,
  ControlSchema,
  InterruptedSchema,
  PingSchema,
  PongSchema,
  ByeSchema,
  ErrorMsgSchema,
]);
export type ServerToDeviceMsg = z.infer<typeof ServerToDeviceMsgSchema>;

/** Gemini tool-call args for set_robot_state — validated before Control is emitted. */
export const RobotStateArgsSchema = z.object({
  expression: ExpressionSchema,
  action: ActionSchema,
});

export function parseDeviceMsg(raw: string): DeviceToServerMsg | null {
  if (raw.length > MAX_TEXT_MESSAGE_BYTES) return null;
  try {
    const parsed = DeviceToServerMsgSchema.safeParse(JSON.parse(raw));
    return parsed.success ? parsed.data : null;
  } catch {
    return null;
  }
}

export function parseServerMsg(raw: string): ServerToDeviceMsg | null {
  if (raw.length > MAX_TEXT_MESSAGE_BYTES) return null;
  try {
    const parsed = ServerToDeviceMsgSchema.safeParse(JSON.parse(raw));
    return parsed.success ? parsed.data : null;
  } catch {
    return null;
  }
}

// ---------------------------------------------------------------------------
// Reconnect policy (shared by mock + documented for firmware)
// ---------------------------------------------------------------------------
export const RECONNECT = {
  baseMs: 500,
  maxMs: 15_000,
  factor: 2,
  jitter: 0.3, // ±30%
} as const;

export function backoffDelayMs(attempt: number): number {
  const raw = Math.min(
    RECONNECT.baseMs * Math.pow(RECONNECT.factor, attempt),
    RECONNECT.maxMs,
  );
  const jitter = raw * RECONNECT.jitter * (Math.random() * 2 - 1);
  return Math.round(raw + jitter);
}
