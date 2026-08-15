# Pixel Bot — backend + playground mock

Voice-and-vision robot broker (Node/TS on Cloud Run ↔ Gemini Multimodal Live)
plus a browser-based hardware simulator. See `IMPLEMENTATION_PLAN.md` for
decisions and `PROTOCOL.md` for the frozen wire spec firmware targets.

## Quick start (Phase 1 exit criteria in 3 commands)

```bash
pnpm install
pnpm --filter @pixel-bot/protocol build
MODE=echo pnpm run dev:backend        # terminal 1 — echo mode, no API key needed
pnpm run dev:mock                     # terminal 2 — open the printed URL
```

Click **Connect & talk**, allow mic+camera, speak — you hear yourself back
with round-trip latency on screen.

## Gemini mode

```bash
cp apps/backend/.env.example apps/backend/.env   # set GEMINI_API_KEY, MODE=gemini
pnpm run dev:backend
pnpm run dev:mock
```

Speak; Gemini sees your webcam, answers with voice, and the mock renders the
eyes/wheel commands. Interrupt it mid-sentence — barge-in flushes playback.

## Deploy (Cloud Run)

```bash
GCP_PROJECT=your-project MODE=gemini bash apps/backend/deploy.sh
```

Creates the service with `--min-instances=1 --session-affinity --timeout=3600`.
Secrets `pixel-gemini-api-key` and `pixel-device-tokens` must exist in Secret
Manager first.

## Soak test (Phase 3 exit criteria)

```bash
SOAK_MINUTES=30 pnpm run soak    # against localhost; SOAK_URL=wss://… for prod
```

Streams synthetic speech, injects socket kills at random, passes only if it
recovers unattended every time.

## Where things are

- `packages/protocol` — frozen wire protocol v1 (Zod schemas, framing, backoff policy)
- `apps/backend` — broker: auth, session lifecycle, Gemini bridge, cost guard, latency logs
- `apps/playground/pixel-mock` — browser simulator: mic→PCM16, webcam→JPEG-on-scene-change, 24k playback, animated eyes, latency HUD
- Grep `SCALE-SEAM:` for every deliberately deferred scaling decision.
