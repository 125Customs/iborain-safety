# 🛡️ Iborain Safety — Edge AI Public Safety & Crime Elimination Network

**Cloud Run Vision-Language Sentry Broker ↔ Google Gemini (Live API & Gemini 3.7 Flash) ↔ Edge Sentry Nodes (Raspberry Pi Zero 2 W + Sony IMX500 AI Camera)**

Iborain Safety is a decentralized Vision-Language AI public safety and crime elimination platform. Born in Nairobi, Iborain reverses the narrative on urban security by replacing passive surveillance and manual records with an infrastructure-free sentry network mounted across **street light poles, road intersections, arterial transit corridors, commercial logistics hubs, and community perimeters**.

---

## Architecture Overview

```
┌────────────────────────────────────────────────────────┐
│               IBORAIN SAFETY CLOUD BRAIN               │
│       Google Cloud Run ↔ Gemini 3.7 Flash / Live       │
└──────────────────────────▲─────────────────────────────┘
                           │ WebSocket (Protocol v1)
                           │ • AudioIn (16kHz PCM from Sentry Mic)
                           │ • Jpeg (Vision diffs from Sony IMX500)
                           │ • AudioOut (24kHz Acoustic Warning/Chime)
                           │ • JSON Control {threatLevel, deterrence, fingerprint}
┌────────────────────────────────────────────────────────┐
│             TACTICAL SENTRY NODE (CHIPUROBO LAB)       │
│  • Raspberry Pi Zero 2 W (Quad-Core 64-bit ARM)        │
│  • Sony IMX500 AI Camera (On-Sensor Neural DSP & ROI)  │
│  • Quectel 4G LTE HAT + High-Gain External SMA Antenna │
│  • MPU-6500 6-Axis IMU (Anti-Tamper / Anti-Theft)      │
│  • Stealth Weatherproof PETG Enclosure (Zero Lights)   │
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

## Live Gemini Mode

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
- `IBORAIN_MASTER_SPECIFICATION.md` — Complete master project specification, commercial model, and XPRIZE Devpost submission blueprint.
