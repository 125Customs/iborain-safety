# Iborain Safety — Implementation Plan (Pre-Seed Edition)

**Status:** Phases 1–4 scaffolded and fully implemented in this monorepo. Deployment and live Gemini Live / 3.7 Flash testing require your GCP project and `GEMINI_API_KEY`.

---

## 1. Architectural Decisions & Tradeoffs

| Decision | Choice | Why / Tradeoff |
|---|---|---|
| **Gemini Models** | `gemini-3.7-flash` & `gemini-2.5-flash-native-audio-preview` | `gemini-3.7-flash` delivers $0.75/1M token pricing and 30.4% AutomationBench reasoning for FreeForm crime search; Live model provides sub-600ms native audio/tool edge streaming. |
| **Control JSON Transport** | Gemini **function calling** (`set_sentry_state` tool, `behavior: NON_BLOCKING`, `scheduling: SILENT`) | Native Live models communicate via `AUDIO` responses; tool calls provide structured forensic telemetry. Backend Zod-validates arguments; invalid calls are dropped and logged. |
| **Wire Framing** | Binary WS frames with 9-byte header: `[1B type][8B uint64 LE capture-ts ms]` + payload; JSON text frames for control plane | Eliminates base64 overhead (~33% bandwidth savings), simple parsing on embedded Linux / C++, capture timestamps enable exact hop-by-hop latency logging. |
| **Audio Pipeline** | In: 16kHz PCM16 mono LE (native Gemini input rate). Out: **24kHz** PCM16 (Gemini native output; edge I2S clocks at 24kHz for playback) | Zero transcoding latency on device or cloud broker. |
| **Gemini 2-Min Audio/Video Session Cap** | Transparent cloud-side **session resumption** (resumption handle + context window compression) on `goAway` or disconnect | Ensures continuous 24/7 sentry monitoring without edge reconnect storms. |
| **Session State** | In-process `Map<deviceId, Session>` | Sufficient for single-instance demo and regional deployment with Cloud Run session affinity. `// SCALE-SEAM: Redis/Firestore for multi-region shards`. |
| **Cost & Quota Controls** | Token bucket + per-session hard caps + daily budget kill-switch fed by Gemini `usageMetadata` | Prevents runaway costs; logged per session close. |
| **Edge Anti-Tamper Safety** | 6-Axis MPU-6500 IMU vibration/pry interrupt + on-sensor IMX500 Neural ROI arrival trigger | Instant edge-level detection operates with $<5\text{ms}$ latency independent of network connectivity. |
| **Echo Mode** | `MODE=echo` runs local loopback verification without burning Gemini API quota | Measures baseline infrastructure latency floor before live AI deployment. |

---

## 2. Repo Layout

```
smartB0t/
├── packages/
│   └── protocol/              # Frozen wire spec: Zod schemas, binary framing, threat enums
├── apps/
│   ├── backend/               # Google Cloud Run Broker (Gemini 3.7 Flash & Live Bridge)
│   │   ├── src/               # gemini.ts, session.ts, bridge.ts, cost-guard.ts, latency.ts
│   │   ├── scripts/soak-test.ts # 30-min automated soak test with fault injection
│   │   └── Dockerfile, deploy.sh
│   ├── playground/
│   │   └── pixel-mock/        # Browser Sentry Intelligence Portal (Vite + Web Audio)
│   └── pi-client/             # Raspberry Pi Zero 2 Native Sentry Client
│       ├── test_hardware.py   # One-command smoke test (I2C scan + GC9A01 sentry beacon)
│       └── robot.py           # Live WebSocket sentry streaming Camera/Mic to Gemini
├── PROTOCOL.md                # Frozen wire specification (v1)
├── IBORAIN_MASTER_SPECIFICATION.md # Master project spec, GTM, and XPRIZE narrative
└── IMPLEMENTATION_PLAN.md     # Architecture decisions & cost caps
```

---

## 3. Latency Budget (<800ms Perceived Turnaround)

Timestamps logged at: device capture $\rightarrow$ broker-in $\rightarrow$ gemini-send $\rightarrow$ gemini-first-audio $\rightarrow$ broker-out $\rightarrow$ device playback-start. Per-turn breakdown is logged as a structured Pino JSON log (`event: "turn_latency"`).

---

## 4. Cost Controls & Token Conservation

1. **Scene-Change & Arrival Throttling**: Edge cameras send frames only when the Sony IMX500 on-sensor Neural ROI detects an entering vehicle/motorcycle, capped at $\le$1 fps.
2. **Hard Session Lifecycle**: 10-minute session cap $\rightarrow$ clean re-handshake. 60-second acoustic silence $\rightarrow$ idle sleep (`audioStreamEnd` sent at 1s pause to flush Gemini VAD).
3. **Daily Budget Enforcement**: Per-device daily spending limit enforced via `usageMetadata` token accounting.
