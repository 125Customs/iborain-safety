/**
 * @iborain/protocol — FROZEN wire protocol v1.
 * Tactical public safety and transit forensics wire protocol for Iborain Safety.
 */
import { z } from "zod";

export const PROTOCOL_VERSION = 1;
export const AUDIO_IN_SAMPLE_RATE = 16000;
export const AUDIO_OUT_SAMPLE_RATE = 24000;
export const MAX_AUDIO_FRAME_BYTES = 32000; // 1s of 16kHz PCM16
export const MAX_JPEG_FRAME_BYTES = 500000;  // 500 KB limit for edge diffs

// Frame types for binary WebSocket protocol.
export enum FrameType {
  AudioIn = 0x01,  // 16kHz PCM16 LE mono (sentry acoustic stream)
  Jpeg = 0x02,     // JPEG image (vision frame diff from Sony IMX500)
  AudioOut = 0x03, // 24kHz PCM16 LE mono (acoustic deterrent / chime)
}

// 9-byte binary header: [1B type][8B uint64 LE capture-timestamp ms]
export const HEADER_SIZE = 9;

export interface BinaryFrame {
  type: FrameType;
  captureTsMs: number;
  payload: Uint8Array;
}

export function encodeHeader(type: FrameType, captureTsMs: number): Uint8Array {
  const buf = new Uint8Array(HEADER_SIZE);
  buf[0] = type;
  const view = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
  view.setBigUint64(1, BigInt(Math.max(0, Math.floor(captureTsMs))), true);
  return buf;
}

export function decodeHeader(data: Uint8Array): { type: FrameType; captureTsMs: number } {
  if (data.byteLength < HEADER_SIZE) {
    throw new Error(`Frame too small for header: ${data.byteLength} < ${HEADER_SIZE}`);
  }
  const type = data[0] as FrameType;
  const view = new DataView(data.buffer, data.byteOffset, data.byteLength);
  const captureTsMs = Number(view.getBigUint64(1, true));
  return { type, captureTsMs };
}

export function encodeBinaryFrame(frame: BinaryFrame): Uint8Array {
  const out = new Uint8Array(HEADER_SIZE + frame.payload.byteLength);
  out.set(encodeHeader(frame.type, frame.captureTsMs), 0);
  out.set(frame.payload, HEADER_SIZE);
  return out;
}

export function decodeBinaryFrame(buf: Uint8Array): BinaryFrame {
  const { type, captureTsMs } = decodeHeader(buf);
  const payload = buf.subarray(HEADER_SIZE);
  return { type, captureTsMs, payload };
}

export function backoffDelayMs(attempt: number, baseMs = 250, maxMs = 4000, jitter = 0.2): number {
  const exp = Math.min(baseMs * 2 ** attempt, maxMs);
  const r = (Math.random() * 2 - 1) * jitter;
  return Math.max(0, Math.floor(exp * (1 + r)));
}

// Tactical Threat Levels
export const ThreatLevelSchema = z.enum(["CLEAR", "SUSPICIOUS", "HOTLIST_MATCH", "EMERGENCY"]);
export type ThreatLevel = z.infer<typeof ThreatLevelSchema>;

// Active Deterrence Actions
export const DeterrenceActionSchema = z.enum([
  "IDLE_BEACON",
  "VERIFIED_GREEN",
  "STROBE_ALERT",
  "ACOUSTIC_WARNING",
  "POLICE_SIREN",
]);
export type DeterrenceAction = z.infer<typeof DeterrenceActionSchema>;

// African Transit Vehicle Types
export const VehicleTypeSchema = z.enum([
  "car",
  "boda_boda",
  "matatu",
  "truck",
  "pedestrian",
]);
export type VehicleType = z.infer<typeof VehicleTypeSchema>;

// African Transit Forensic Fingerprint
export const TransitFingerprintSchema = z.object({
  plate: z.string(), // "KDA 482B", "KMDF 892Z", or "UNPLATED"
  vehicleType: VehicleTypeSchema,
  confidence: z.number().min(0).max(1),
  traits: z.string(), // e.g. "White Toyota Probox, tinted rear, roof rack"
  bodaDetails: z
    .object({
      helmet: z.boolean().optional(),
      reflectorJacket: z.string().optional(),
      passengerCount: z.number().int().optional(),
      cargo: z.string().optional(), // e.g. "13kg blue gas cylinder"
    })
    .optional(),
  hotlistMatch: z.boolean().default(false),
  hotlistReason: z.string().optional(),
});
export type TransitFingerprint = z.infer<typeof TransitFingerprintSchema>;

// JSON Control Plane Messages (server -> sentry client)
export const SentryStateArgsSchema = z.object({
  threatLevel: ThreatLevelSchema,
  deterrence: DeterrenceActionSchema,
  message: z.string(),
  audioPrompt: z.string().optional(),
  plate: z.string().optional(),
  vehicleType: VehicleTypeSchema.optional(),
  traits: z.string().optional(),
  bodaCargo: z.string().optional(),
  hotlistMatch: z.boolean().optional(),
  hotlistReason: z.string().optional(),
});
export type SentryStateArgs = z.infer<typeof SentryStateArgsSchema>;

export const ControlSchema = z.object({
  type: z.literal("control"),
  threatLevel: ThreatLevelSchema,
  deterrence: DeterrenceActionSchema,
  message: z.string(),
  audioPrompt: z.string().optional(),
  fingerprint: TransitFingerprintSchema.optional(),
  turnId: z.string(),
});
export type Control = z.infer<typeof ControlSchema>;

export const InterruptedSchema = z.object({
  type: z.literal("interrupted"),
  turnId: z.string().optional(),
});
export type Interrupted = z.infer<typeof InterruptedSchema>;

export const TurnCompleteSchema = z.object({
  type: z.literal("turn_complete"),
  turnId: z.string(),
});
export type TurnComplete = z.infer<typeof TurnCompleteSchema>;

export const HelloAckSchema = z.object({
  type: z.literal("hello_ack"),
  proto: z.number(),
  sessionId: z.string(),
  sampleRateIn: z.number().default(AUDIO_IN_SAMPLE_RATE),
  sampleRateOut: z.number().default(AUDIO_OUT_SAMPLE_RATE),
  budgetRemainingMs: z.number().default(0),
});
export type HelloAck = z.infer<typeof HelloAckSchema>;

export const ByeSchema = z.object({
  type: z.literal("bye"),
  reason: z.string(),
});
export type Bye = z.infer<typeof ByeSchema>;

export const PingSchema = z.object({
  type: z.literal("ping"),
  ts: z.number(),
});
export type Ping = z.infer<typeof PingSchema>;

export const ErrorSchema = z.object({
  type: z.literal("error"),
  code: z.string(),
  message: z.string(),
});
export type ErrorMsg = z.infer<typeof ErrorSchema>;

export const ServerMessageSchema = z.discriminatedUnion("type", [
  HelloAckSchema,
  ControlSchema,
  InterruptedSchema,
  TurnCompleteSchema,
  ByeSchema,
  PingSchema,
  ErrorSchema,
]);
export type ServerMessage = z.infer<typeof ServerMessageSchema>;
export type ServerToDeviceMsg = ServerMessage;

export function parseServerMsg(raw: string): ServerMessage {
  const json = JSON.parse(raw);
  return ServerMessageSchema.parse(json);
}

// JSON Client Messages (sentry client -> server)
export const HelloSchema = z.object({
  type: z.literal("hello"),
  proto: z.number(),
  deviceId: z.string(),
  fw: z.string().optional(),
});
export type Hello = z.infer<typeof HelloSchema>;

export const ClientEventSchema = z.object({
  type: z.literal("event"),
  event: z.enum([
    "arrival_triggered",
    "tripwire_broken",
    "tamper_detected",
    "manual_override",
    "playback_started",
    "playback_finished",
  ]),
  timestampMs: z.number(),
  metadata: z.record(z.unknown()).optional(),
});
export type ClientEvent = z.infer<typeof ClientEventSchema>;

export const PlaybackStartedSchema = z.object({
  type: z.literal("playback_started"),
  turnId: z.string(),
  ts: z.number(),
});
export type PlaybackStarted = z.infer<typeof PlaybackStartedSchema>;

export const PongSchema = z.object({
  type: z.literal("pong"),
  ts: z.number(),
});
export type Pong = z.infer<typeof PongSchema>;

export const ClientMessageSchema = z.discriminatedUnion("type", [
  HelloSchema,
  ClientEventSchema,
  PlaybackStartedSchema,
  PingSchema,
  PongSchema,
]);
export type ClientMessage = z.infer<typeof ClientMessageSchema>;

export function parseClientMsg(raw: string): ClientMessage {
  const json = JSON.parse(raw);
  return ClientMessageSchema.parse(json);
}
export const parseDeviceMsg = parseClientMsg;
