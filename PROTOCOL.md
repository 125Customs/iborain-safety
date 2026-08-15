# Pixel Bot Wire Protocol — v1 (FROZEN)

This document is the single source of truth for firmware. Implement against
this file; do not read backend code. The reference implementation of every
schema and constant is `packages/protocol/src/index.ts` — if this doc and that
file ever disagree, the package wins and this doc must be fixed.

## Transport

- WebSocket over TLS: `wss://<host>/?device=<deviceId>&token=<bearerToken>`
- Auth: `token` query param (or `Authorization: Bearer <token>` header).
  Bad/missing token → HTTP 401 at upgrade. Reconnect storm → 429. Daily budget
  spent → 402 (back off ≥1 hour).
- One connection per device. A new connection from the same deviceId replaces
  the old one server-side.

## Safety (non-negotiable)

The backend is NEVER in the safety path. `action` commands are advisory
locomotion suggestions. Firmware MUST gate all wheel output behind the
CD4069UBE cliff-sensor hardware cut-off loop. Loss of connection, garbage
data, or a malicious server must never be able to drive the robot off a table.

## Message kinds

Two kinds of WebSocket messages:

1. **Binary frames** — audio and camera data.
2. **Text frames** — JSON control plane, UTF-8, max 4096 bytes.

### Binary frame layout

```
byte 0        : frame type (uint8)
bytes 1..8    : capture timestamp, ms since Unix epoch, uint64 little-endian
bytes 9..end  : payload
```

| Type | Value | Direction | Payload | Max payload |
|---|---|---|---|---|
| AudioIn | `0x01` | device → server | raw PCM, 16-bit signed LE, mono, **16 kHz** | 32768 B |
| Jpeg | `0x02` | device → server | JPEG image (camera frame) | 307200 B |
| AudioOut | `0x11` | server → device | raw PCM, 16-bit signed LE, mono, **24 kHz** | — |

Notes for firmware:
- Send mic audio in ~100 ms chunks (3200 B payload at 16 kHz PCM16).
- **Playback is 24 kHz** (Gemini native output rate) — clock the I2S/MAX98357A
  at 24000 Hz for playback. Input stays 16 kHz.
- Oversized frames are dropped server-side (and logged), not fatal.
- Camera frames: max 1 fps, and only when the scene changed. Reference
  algorithm (mock uses the same): downscale to 64×48 grayscale-ish, mean
  absolute pixel delta vs previous frame > 12 → changed; also send a keyframe
  every 10 s regardless. This is a cost control — Gemini bills vision tokens.

### JSON messages — device → server

All messages are validated with Zod server-side; invalid messages get an
`error` reply and are dropped.

```jsonc
// First message after socket opens. Required before any binary frame.
{ "type": "hello", "proto": 1, "deviceId": "pixel-001", "fw": "0.1.0" }

// Application heartbeat (optional; server also uses WS ping/pong opcodes —
// reply to WS pings at the library level).
{ "type": "ping", "ts": 1760000000000 }
{ "type": "pong", "ts": 1760000000000 }

// Report the moment the speaker starts playing a turn's audio
// (closes the end-to-end latency measurement loop).
{ "type": "playback_started", "turnId": "pixel-001-t4", "ts": 1760000000000 }
```

### JSON messages — server → device

```jsonc
// Reply to hello.
{ "type": "hello_ack", "proto": 1, "sessionId": "…", "budgetRemainingMs": 540000 }

// Robot control. Apply expression to the LCD; action is advisory (see Safety).
// expression: neutral | happy | sad | curious | surprised | thinking | sleepy
// action:     none | stop | forward | backward | turn_left | turn_right | wiggle
{ "type": "control", "expression": "happy", "action": "wiggle", "turnId": "pixel-001-t4" }

// Barge-in: the user interrupted the robot. IMMEDIATELY flush the audio
// playback buffer and silence the speaker. Do not finish queued audio.
{ "type": "interrupted", "turnId": "pixel-001-t4" }

// Heartbeat
{ "type": "ping", "ts": 1760000000000 }   // reply with pong, same ts
{ "type": "pong", "ts": 1760000000000 }

// Server is closing the session. Reconnect after retryAfterMs.
// reason: session_cap | idle_timeout | budget_exhausted | server_shutdown |
//         auth_revoked | protocol_error
{ "type": "bye", "reason": "session_cap", "retryAfterMs": 0 }

// Non-fatal notice.
{ "type": "error", "code": "invalid_message", "message": "…" }
```

## Connection lifecycle (firmware state machine)

```
BOOT → CONNECT (wss + token)
  on open        → send hello → await hello_ack → STREAMING
  on 401/402/429 → SLEEPY_FACE, retry per retry rules below
STREAMING
  mic audio      → AudioIn frames continuously while sound is present
  camera         → Jpeg frames on scene-change, ≤1 fps
  AudioOut       → I2S playback queue (24 kHz)
  control        → update eyes + (hardware-gated) wheels
  interrupted    → flush playback queue NOW
  bye            → close; reconnect after retryAfterMs
  socket lost    → SLEEPY_FACE + reconnect with backoff
RECONNECT BACKOFF
  delay = min(500ms × 2^attempt, 15s) ± 30% jitter, reset on success
SLEEPY_FACE (degraded mode)
  eyes = sleepy, wheels stopped; keep retrying in background
```

Heartbeats: server pings every 10 s; if the device misses pongs for 30 s the
server terminates. Firmware should treat 30 s without any server traffic as a
dead socket and reconnect.

Session caps (expected, not errors): 10 min hard cap → `bye(session_cap)` with
`retryAfterMs: 0` → reconnect immediately (fresh session, conversation context
is NOT preserved). 60 s of mic silence → `bye(idle_timeout)`.

## Versioning

`proto` field in `hello` must equal `1`. A server that can't accept the
version closes with `bye(protocol_error)`. Any breaking change to this file
bumps the version.
