# Iborain Safety — Agent Demo Recording & Screen Execution Guide

> **Purpose:** Operational runbook and reference context for AI agents and developers executing live video demos, terminal screen recordings, and GC9A01 LCD hardware demonstrations for the Iborain Safety AI Edge Sentry system.

---

## 1. Key Context & System Architecture

### 1.1 Hardware Specifications (Edge Node)
* **Processor:** Raspberry Pi Zero 2 W (Quad-core 64-bit ARM Cortex-A53 @ 1.0 GHz).
* **Vision Sensor:** Sony IMX500 Intelligent Vision Sensor (On-Sensor Neural DSP, CSI-2 2-Lane, 1080p @ 30fps).
* **Anti-Tamper IMU:** InvenSense MPU-6500 6-Axis Accelerometer & Gyroscope ($I^2C$ address `0x68` / `0x69`, SDA Pin 3, SCL Pin 5).
* **Tactical Diagnostic HUD (Optional):** Waveshare GC9A01 1.28-inch Round TFT LCD ($240 \times 240$ RGB565, SPI 40 MHz, DC Pin 24, RST Pin 25).
* **Power & Network:** 5V / 3A DC input, LTE Cat-1 4G Cellular modem / Wi-Fi fallback.

### 1.2 Telemetry & Forensic Data Context
When generating logs, simulated telemetry, or HUD updates, use the following standardized Kenyan context:

| Metric / Field | Standard Demonstration Value | Notes |
| :--- | :--- | :--- |
| **Device ID** | `sentry-nairobi-001` / `sentry-nairobi-gate-01` | Edge node identifier |
| **Firmware** | `sentry-1.0.0 (Stealth build v2.4.1)` | Embedded Linux edge daemon |
| **Session Protocol** | `@pixel-bot/protocol v1` over TLS 1.3 WebSocket | Binary framing + JSON control |
| **Resident Match** | `KDE 842X` — White Toyota Land Cruiser Prado (2021) | Status: `CLEARED: RESIDENT_AUTH` (Unit #402 Dr. Kamau) |
| **Delivery Match** | `KBY 120Z` — Silver Isuzu D-Max Double Cabin | Status: `CLEARED: DELIVERY_REGISTERED` (DHL Express) |
| **Hotlist Threat** | `KDF 441A` — Black Subaru Forester XT | Status: `🚨 HOTLIST_ALERT: STOLEN_VEHICLE_APB #2026-901` |
| **Inference Latency** | `129ms` to `168ms` (Mean: `142ms`) | End-to-end edge optical $\rightarrow$ Gemini $\rightarrow$ Edge |
| **Inference Cost** | `$0.0014 USD` per classification event | Google Cloud Run + Gemini 2.0 Flash token pricing |

---

## 2. Terminal & Screen Execution Commands

### 2.1 Running the Edge Sentry Terminal & LCD HUD Simulator

The simulator (`apps/pi-client/demo_sentry.py`) outputs ANSI colorized terminal logs and simultaneously drives the physical GC9A01 Round LCD screen (if connected via SPI):

```bash
# Standard single run with all scenarios (Resident -> Delivery -> Stolen APB -> Tamper):
python3 apps/pi-client/demo_sentry.py

# Continuous loop for video takes (keeps running indefinitely):
python3 apps/pi-client/demo_sentry.py --loop

# Faster playback (1.5x speed) or slower (0.8x speed):
python3 apps/pi-client/demo_sentry.py --speed 1.5 --loop

# Trigger a specific scenario on demand:
python3 apps/pi-client/demo_sentry.py --scenario resident
python3 apps/pi-client/demo_sentry.py --scenario stolen
python3 apps/pi-client/demo_sentry.py --scenario tamper

# Or use the integrated flag in robot.py:
python3 apps/pi-client/robot.py --demo
```

---

### 2.2 Running Multi-Terminal Video Demo Layout

For video recording, split your screen into the following 3 windows or terminal panes:

```
┌──────────────────────────────────────────────┬──────────────────────────────────────────────┐
│ PANE 1: Edge Sentry Terminal (Pi SSH / Mac)   │ PANE 2: Cloud Run Backend Broker / AI Brain  │
│                                              │                                              │
│ $ python3 apps/pi-client/demo_sentry.py --loop│ $ pnpm run dev:backend                       │
│                                              │ (or JSON log stream simulator)               │
├──────────────────────────────────────────────┴──────────────────────────────────────────────┤
│ PANE 3: Web Simulator / WhatsApp Dispatch Live Dashboard (Browser at localhost:5173)         │
│                                                                                             │
│ $ pnpm run dev:mock                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

#### Pane 2 Command (Backend JSON Streamer):
```bash
python3 -c "
import time, random, json
devices = ['sentry-nairobi-001', 'sentry-karen-005', 'sentry-ruiru-003']
plates = ['KDE 842X', 'KBY 120Z', 'KDF 441A', 'KCA 778P']
while True:
    d = random.choice(devices)
    p = random.choice(plates)
    lat = random.randint(128, 172)
    print(json.dumps({'timestamp': int(time.time()*1000), 'severity': 'INFO', 'device': d, 'event': 'MULTIMODAL_INFERENCE', 'plate': p, 'latencyMs': lat, 'costUSD': 0.0014, 'verdict': 'CLEARED'}), flush=True)
    time.sleep(random.uniform(0.4, 0.9))
"
```

#### Pane 3 Command (Vite Playground / Simulator):
```bash
pnpm run dev:mock
```

---

## 3. Raspberry Pi Remote Deployment & Verification

When running on physical hardware via SSH:

### 3.1 Sync Code to the Raspberry Pi
From your local Mac terminal:
```bash
rsync -avz --exclude 'node_modules' --exclude '.venv' apps/pi-client/ smartbotpi@smartbotpi.local:~/smartB0t/apps/pi-client/
```

### 3.2 Execute Hardware Verification on Pi
Inside the SSH session (`smartbotpi@smartbotpi.local`):
```bash
# 1. Test I2C bus and IMU sensor detection:
python3 apps/pi-client/test_hardware.py

# 2. Launch the demo screen & terminal feed:
python3 apps/pi-client/demo_sentry.py --loop
```

---

## 4. Video Recording Best Practices

1. **Terminal Typography:** Use *JetBrains Mono Nerd Font* or *Fira Code* at **15pt** font size.
2. **Terminal Theme:** Dark high-contrast palette (*Tokyo Night*, *Catppuccin Mocha*, or *One Dark*).
3. **Camera Alignment:** If filming the physical Raspberry Pi + 1.28" Round LCD screen, place the camera at a **45-degree isometric angle** with clean diffused desk lighting to avoid glare on the display lens.
4. **Clean Cut Points:** Use the `--- [CYCLE N COMPLETE] ---` log line as the transition marker between video scenes.
