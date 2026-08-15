# Pixel Bot — Implementation Plan (Pre-Seed Edition)

Status: Phases 1–4 scaffolded and implemented in this monorepo. Deploy + live Gemini testing require your GCP project and `GEMINI_API_KEY`.

## Judged against the three questions

Every module below either improves the demo, cuts Gemini COGS, or is a config-change seam. Deferred items are absent by design and marked `// SCALE-SEAM:` at their plug-in points.

## Key decisions & assumptions

| Decision | Choice | Why / tradeoff |
|---|---|---|
| Gemini model | `gemini-2.5-flash-native-audio-preview-12-2025` (env `GEMINI_MODEL`) | Native audio out (skip TTS hop) **and** NON_BLOCKING async function calling, so `{expression, action}` commands stream alongside speech. `gemini-3.1-flash-live-preview` has lower thinking latency but *blocking* tool calls — it would stall speech on every expression change. Swap = one env var. |
| Control JSON transport | Gemini **function calling** (`set_robot_state` tool, `behavior: NON_BLOCKING`, `scheduling: SILENT`) | Native-audio Live models only support `AUDIO` response modality — no response schema. Tool calls are the documented path. Broker Zod-validates args; invalid → dropped + logged, never forwarded. |
| Wire framing | Binary WS frames, 9-byte header: `[1B type][8B uint64 LE capture-ts ms]` + payload; JSON text frames for control plane | No base64 (~33% saved), trivial for ESP32 C++, capture timestamp enables true end-to-end latency per hop. |
| Audio | In: 16kHz PCM16 mono LE (exactly what Live API wants — zero transcode). Out: **24kHz** PCM16 (Live API native output; firmware I2S must clock 24k on playback) | No Opus for v1 per spec. `// SCALE-SEAM: Opus transcoding pipeline`. |
| Gemini 2-min audio+video session cap | Broker performs transparent Gemini-side **session resumption** (resumption handle + context) on `goAway`/expiry; device socket unaffected | Doc'd hard limit; without this the robot dies mid-demo at 2:00. Moved from Phase 3 → Phase 2 (demo-critical). |
| Session state | In-process `Map<deviceId, Session>` | `// SCALE-SEAM: externalize (Redis/Firestore) when we shard`. Cloud Run session affinity + min-instances=1 makes this safe at demo scale. |
| Rate/cost control | In-memory token bucket + per-session hard caps + daily budget kill-switch fed by `usageMetadata` token counts | `// SCALE-SEAM: swap for Upstash Redis`. |
| Auth | Static per-device bearer tokens (env/Secret Manager JSON map), checked at WS upgrade | Nothing fancier yet. `// SCALE-SEAM: ephemeral tokens / device provisioning`. |
| Echo mode | `MODE=echo` env runs the Phase-1 walking skeleton (no Gemini, audio loopback) | Deploy day 1, measure infra latency floor before burning Gemini quota. |

## Repo layout

```
pixel-bot/
├─ packages/protocol/          # frozen wire spec: Zod schemas, binary framing, enums, version
├─ apps/backend/               # Cloud Run broker (echo mode + Gemini bridge)
│  ├─ src/{config,logger,auth,server,session,gemini,cost-guard,latency}.ts
│  ├─ scripts/soak-test.ts     # 30-min unattended soak w/ socket-kill injection
│  ├─ Dockerfile  deploy.sh
├─ apps/playground/pixel-mock/ # browser mock: mic→PCM16, webcam→JPEG-on-scene-change, eyes, latency HUD
├─ PROTOCOL.md                 # firmware implements against this, not backend code
└─ IMPLEMENTATION_PLAN.md
```

## Latency budget (<800ms perceived)

Timestamps logged at: device capture → broker-in → gemini-send → gemini-first-audio → broker-out → device playback-start. Per-turn breakdown logged as one Pino line (`event: "turn_latency"`). Mock prints round-trip on screen. Levers if over budget: `silence_duration_ms` VAD tuning (500ms default), `thinkingBudget: 0`, media resolution LOW, region-pin Cloud Run near Gemini endpoint.

## Cost controls (biggest COGS)

Hard session cap 10 min → polite re-handshake. Idle disconnect 60s of silence (`audioStreamEnd` sent at 1s pause to flush VAD). Camera frames only on scene-change (mock: frame-diff threshold; firmware: same algorithm doc'd in PROTOCOL.md), ≤1 fps (API max anyway). Daily per-device budget kill-switch from `usageMetadata`. $/hr estimate logged per session close.

## Explicitly NOT built (seams only)

Upstash Redis, session-state encryption beyond TLS+tokens, Opus, multi-region, session migration, admin dashboards. Grep `SCALE-SEAM:` for every plug-in point.

## Open questions (non-blocking, assumptions stated inline)

1. **GCP project/region** — deploy.sh assumes `us-central1`; edit one variable.
2. **Voice** — defaulted to `Puck` (playful); env `GEMINI_VOICE`.
3. **Daily budget** — defaulted $5/device/day; env `DAILY_BUDGET_USD`.
4. **Safety**: backend is never in the safety path — cliff cut-off stays in the CD4069 hardware loop. `action` commands are advisory locomotion only; firmware must gate them behind the hardware loop. Stated in PROTOCOL.md.

## Phase exit criteria mapping

- **P1**: `MODE=echo pnpm dev` + mock → hear yourself, RTT on screen. ✅ implemented
- **P2**: full conversation, webcam vision, control JSON rendered, per-turn latency logged. ✅ implemented (needs API key to run live)
- **P3**: soak script survives 30 min with injected socket kills; $/hr known from logs. ✅ implemented
- **P4**: PROTOCOL.md frozen, version field `1`. ✅
