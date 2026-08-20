# Iborain Safety Wire Protocol — v1 (FROZEN)

**Status:** FROZEN  
**Transport:** WebSocket over TLS (`wss://`)  
**Framing:** Binary WebSocket frames with 9-byte header for audio/vision streaming; JSON text frames for control plane.

---

## 1. Binary Frame Header (9 Bytes)

All binary frames have a fixed 9-byte header:

```
[0]     : uint8  FrameType (0x01 = AudioIn, 0x02 = Jpeg, 0x03 = AudioOut)
[1..8]  : uint64 LE capture timestamp (ms since UNIX epoch)
[9..N]  : payload (raw PCM16 LE or JPEG bytes)
```

### Frame Types:
- `0x01` (`AudioIn`): Sentry microphone capture. **Format:** 16kHz, 16-bit mono PCM LE.
- `0x02` (`Jpeg`): Sentry camera frame diffs (Sony IMX500 / Pi Cam). **Format:** JPEG, $\le$1 fps.
- `0x03` (`AudioOut`): Cloud warning / acoustic siren / speech. **Format:** 24kHz, 16-bit mono PCM LE.

---

## 2. JSON Control Messages (Server $\rightarrow$ Sentry Client)

### Sentry Threat Control (`control`):
```json
{
  "type": "control",
  "threatLevel": "HOTLIST_MATCH",
  "deterrence": "STROBE_ALERT",
  "message": "SUSPECT BODA FLAGGED",
  "audioPrompt": "Warning: Vehicle flagged on community crime watch.",
  "fingerprint": {
    "plate": "KMDF 892Z",
    "vehicleType": "boda_boda",
    "confidence": 0.96,
    "traits": "Red Boxer 150, black courier backpack",
    "bodaDetails": {
      "helmet": false,
      "cargo": "13kg blue gas cylinder"
    },
    "hotlistMatch": true,
    "hotlistReason": "Armed burglary getaway suspect"
  },
  "turnId": "turn-1723891200000"
}
```

---

## 3. JSON Client Events (Sentry Client $\rightarrow$ Server)

```json
{
  "type": "event",
  "event": "arrival_triggered",
  "timestampMs": 1723891200000,
  "metadata": { "sensor": "IMX500_NEURAL_ROI", "gateId": "syokimau-gate-1" }
}
```
