# BomaSafety Wire Protocol — v1 (FROZEN)

This document is the single source of truth for edge sentry firmware and client runtimes. Implement against this file. The reference implementation of every schema and constant is `packages/protocol/src/index.ts`.

## Transport

- WebSocket over TLS: `wss://<host>/?device=<deviceId>&token=<bearerToken>`
- Auth: `token` query param (or `Authorization: Bearer <token>` header).
  Bad/missing token → HTTP 401 at upgrade. Reconnect storm → 429. Daily budget spent → 402 (back off ≥1 hour).
- One connection per sentry unit. A new connection from the same `deviceId` replaces the old one server-side.

## Tactical Safety & Edge Autonomy

The cloud backend provides perceptual and investigative reasoning. Hardware-level physical triggers (such as the CD4069UBE tamper loop and TCRT5000 optical arrival tripwire) execute locally with **0ms latency**, independent of network connectivity.

## Message Kinds

Two kinds of WebSocket messages:

1. **Binary frames** — audio stream and camera frames.
2. **Text frames** — JSON control and threat dispatch plane, UTF-8, max 4096 bytes.

### Binary Frame Layout

```
byte 0        : frame type (uint8)
bytes 1..8    : capture timestamp, ms since Unix epoch, uint64 little-endian
bytes 9..end  : payload
```

| Type | Value | Direction | Payload | Max Payload |
|---|---|---|---|---|
| AudioIn | `0x01` | device → server | raw PCM, 16-bit signed LE, mono, **16 kHz** | 32768 B |
| Jpeg | `0x02` | device → server | JPEG image (Sony IMX500 / Pi Cam frame) | 307200 B |
| AudioOut | `0x11` | server → device | raw PCM, 16-bit signed LE, mono, **24 kHz** | — |

#### Sentry Hardware Rules:
- Stream ambient mic audio in ~100 ms chunks (3200 B payload at 16 kHz PCM16).
- **Audio playback is 24 kHz** (Gemini native voice/chime output) — clock the I2S / MAX98357A DAC at 24000 Hz for playback.
- **Camera frames**: Sent on vehicle arrival / scene-change, max 1 fps. Frame-diff threshold algorithm: downscale to 64×48 grayscale, mean absolute pixel delta > 12 → send frame; plus keyframe every 10s.

### JSON Messages — Device → Server

All messages are validated with Zod server-side.

```jsonc
// 1. Handshake after socket opens (Required before binary streaming)
{ "type": "hello", "proto": 1, "deviceId": "sentry-nairobi-001", "fw": "1.0.0" }

// 2. Application heartbeat
{ "type": "ping", "ts": 1760000000000 }
{ "type": "pong", "ts": 1760000000000 }

// 3. Playback confirmation (closes end-to-end latency measurement loop)
{ "type": "playback_started", "turnId": "sentry-001-t4", "ts": 1760000000000 }
```

### JSON Messages — Server → Device

```jsonc
// 1. Handshake acknowledgement
{ "type": "hello_ack", "proto": 1, "sessionId": "…", "budgetRemainingMs": 540000 }

// 2. Tactical Sentry Control & Deterrence Command
// threatLevel: CLEAR | SUSPICIOUS | HOTLIST_MATCH | EMERGENCY
// deterrence:  IDLE_BEACON | VERIFIED_GREEN | STROBE_ALERT | ACOUSTIC_WARNING | POLICE_SIREN
{
  "type": "control",
  "threatLevel": "HOTLIST_MATCH",
  "deterrence": "STROBE_ALERT",
  "message": "HOTLIST ALERT — STOLEN BODA KMDF 892Z",
  "audioPrompt": "Warning: Vehicle flagged on community crime watch list. Security dispatched.",
  "fingerprint": {
    "plate": "KMDF 892Z",
    "vehicleType": "boda_boda",
    "confidence": 0.96,
    "traits": "Red Boxer 150, black fuel tank, yellow reflector jacket",
    "bodaDetails": {
      "helmet": true,
      "reflectorJacket": "yellow",
      "passengerCount": 1,
      "cargo": "13kg Blue Gas Cylinder"
    },
    "hotlistMatch": true,
    "hotlistReason": "Flagged in Syokimau Court 3 residential burglary"
  },
  "turnId": "sentry-001-t4"
}

// 3. Barge-In / Interruption
// Immediately flush audio playback buffer and silence the speaker
{ "type": "interrupted", "turnId": "sentry-001-t4" }

// 4. Session termination
// reason: session_cap | idle_timeout | budget_exhausted | server_shutdown | auth_revoked | protocol_error
{ "type": "bye", "reason": "session_cap", "retryAfterMs": 0 }

// 5. Error notice
{ "type": "error", "code": "invalid_message", "message": "…" }
```

## Connection Lifecycle (Sentry Firmware State Machine)

```
BOOT → CONNECT (wss + token)
  on open        → send hello → await hello_ack → ACTIVE_MONITORING
  on 401/402/429 → IDLE_BEACON, retry per exponential backoff
ACTIVE_MONITORING
  mic audio      → AudioIn frames continuously during acoustic events
  camera         → Jpeg frames on vehicle arrival / scene-diff, ≤1 fps
  AudioOut       → I2S playback queue (24 kHz acoustic warnings/chimes)
  control        → update GC9A01 deterrence strobe & threat display
  interrupted    → flush playback queue immediately
  bye            → close socket; reconnect after retryAfterMs
  socket lost    → IDLE_BEACON + reconnect with backoff
RECONNECT BACKOFF
  delay = min(500ms × 2^attempt, 15s) ± 30% jitter, reset on success
```

## Versioning

`proto` field in `hello` must equal `1`. Any breaking change bumps `PROTOCOL_VERSION`.
