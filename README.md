# 🛡️ BomaSafety — Edge AI Public Safety & Crime Elimination Network

**Cloud Run Vision-Language Sentry Broker ↔ Google Gemini Multimodal Live API ↔ Edge Sentry Unit (Raspberry Pi Zero 2 W + Sony IMX500 AI Camera)**

BomaSafety is Africa's first decentralized Vision-Language AI public safety and crime elimination platform. It replaces passive surveillance and manual security records with real-time African transit forensics, inter-community crime hotlist meshes, autonomous acoustic/visual deterrence, and natural-language FreeForm™ crime investigation search.

---

## Architecture Overview

```
┌────────────────────────────────────────────────────────┐
│               BOMASAFETY CLOUD BRAIN                   │
│      Google Cloud Run ↔ Gemini Multimodal Live API     │
└──────────────────────────▲─────────────────────────────┘
                           │ WebSocket (Protocol v1)
                           │ • AudioIn (16kHz PCM from Sentry Mic)
                           │ • Jpeg (Vision diffs from Sony IMX500)
                           │ • AudioOut (24kHz Acoustic Warning/Chime)
                           │ • JSON Control {threatLevel, deterrence, fingerprint}
┌──────────────────────────▼─────────────────────────────┐
│             TACTICAL SENTRY UNIT                       │
│  • Raspberry Pi Zero 2 W + Sony IMX500 AI Camera       │
│  • GC9A01 1.28" Round LCD (Threat Beacon & Strobe)     │
│  • MAX98357A I2S 3W DAC + Acoustic Warning Speaker     │
│  • MPU-6500 6-Axis IMU (Anti-Tamper / Anti-Theft)      │
│  • TCRT5000 IR Tripwire (Zero-Latency Arrival Trigger) │
│  • CD4069UBE CMOS Logic (Hardware Tamper Clamp)        │
└────────────────────────────────────────────────────────┘
```

---

## Quick Start (3 Commands)

```bash
# 1. Install dependencies and build protocol package
pnpm install
pnpm --filter @pixel-bot/protocol build

# 2. Start Broker in Echo Mode (Terminal 1 — no Gemini API key required)
MODE=echo pnpm run dev:backend

# 3. Start Browser Sentry Intelligence Portal (Terminal 2)
pnpm run dev:mock
```

Open the printed URL, click **Activate Sentry & Stream**, allow mic + camera, and test real-time vehicle/transit forensics with round-trip latency HUD.

---

## Live Gemini Multimodal Live Mode

```bash
cp apps/backend/.env.example apps/backend/.env   # Set GEMINI_API_KEY, MODE=gemini
pnpm run dev:backend
pnpm run dev:mock
```

Stream live camera frames; Gemini will analyze plates, vehicle types, Boda Boda helmet compliance, and cargo (gas cylinders, courier bags), triggering active sentry beacons and simulated WhatsApp security broadcasts.

---

## Cloud Run Deployment

```bash
GCP_PROJECT=your-project MODE=gemini bash apps/backend/deploy.sh
```

Deploys to Google Cloud Run with `--min-instances=1 --session-affinity --timeout=3600`.

---

## Automated Soak & Latency Testing

```bash
SOAK_MINUTES=2 pnpm run soak    # Against localhost; SOAK_URL=wss://… for production
```

Simulates high-speed edge sentries, sends synthetic acoustic waveforms, and injects random connection drops to verify 100% unattended recovery.

---

## Repository Structure

- `packages/protocol` — Frozen wire protocol v1 (Zod schemas, framing, threat levels, transit fingerprints).
- `apps/backend` — Google Cloud Run broker: auth, session lifecycle, Gemini Multimodal Live bridge, cost guards, latency telemetry.
- `apps/playground/pixel-mock` — Browser Sentry Intelligence & WhatsApp Dispatch Simulator: mic→PCM16, camera→JPEG diffs, GC9A01 sentry beacon mock, latency HUD.
- `apps/pi-client` — Native Raspberry Pi Zero 2 W Python client (`test_hardware.py`, `robot.py`).
- `BOMASENTRY_MASTER_SPECIFICATION.md` — Complete master project specification, commercial model, and XPRIZE Devpost submission blueprint.
