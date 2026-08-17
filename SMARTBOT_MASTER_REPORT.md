# 🛡️ BomaSafety — Master Project & Submission Report

**Repository:** [https://github.com/bobybarack/smartB0t](https://github.com/bobybarack/smartB0t)  
**Local Monorepo Path:** [`/Users/radebe49/smartB0t`](file:///Users/radebe49/smartB0t)  
**Competition Target:** [Build with Gemini XPRIZE — Devpost ($2,000,000)](https://xprize.devpost.com/)  
**Submission Category:** **Small Business Services**  
**Submission Deadline:** August 17, 2026 @ 1:00 PM PDT  

---

## 1. Executive Summary & Value Proposition

**BomaSafety** is Africa's first decentralized Vision-Language AI public safety and crime elimination network. Powered by the **Google Gemini Multimodal Live API** on Google Cloud Run and edge sentry hardware (Raspberry Pi Zero 2 W + Sony IMX500 AI Camera), BomaSafety captures multimodal African transit fingerprints, detects community crime hotlist matches in real time, executes autonomous acoustic and visual deterrence, and provides natural-language FreeForm™ crime investigation for security teams and detectives.

```
┌────────────────────────────────────────────────────────┐
│               BOMASAFETY CLOUD BRAIN                   │
│      Google Cloud Run ↔ Gemini Multimodal Live API     │
└──────────────────────────▲─────────────────────────────┘
                           │ WebSocket (Protocol v1)
                           │ • AudioIn (16kHz Sentry Mic Stream)
                           │ • Jpeg (Vision diffs < 1fps from IMX500)
                           │ • AudioOut (24kHz Acoustic Warnings/Chimes)
                           │ • JSON Control {threatLevel, deterrence, fingerprint}
┌──────────────────────────▼─────────────────────────────┐
│             TACTICAL SENTRY UNIT                       │
│  • Raspberry Pi Zero 2 W + Sony IMX500 AI Camera       │
│  • GC9A01 1.28" Round LCD (Active Sentry Strobe)       │
│  • MAX98357A I2S DAC + 3W Acoustic Warning Speaker     │
│  • MPU-6500 6-Axis IMU (Anti-Tamper & Anti-Vandalism)  │
│  • TCRT5000 IR Tripwire (Zero-Latency Arrival Trigger) │
│  • CD4069UBE Logic (Hardware Tamper Clamp)             │
└────────────────────────────────────────────────────────┘
```

---

## 2. XPRIZE Alignment & Judging Strategy

| Judging Pillar (Stage 2) | How BomaSafety Wins |
| :--- | :--- |
| **1. Business Viability & Revenue** | **High-Margin Zero-CapEx SaaS:** Free hardware installation + KES 6,500/mo ($49/mo) community safety subscription billed via automated M-Pesa STK Push. 2.2-month installer payback, 51x LTV/CAC. |
| **2. AI-Native Operations** | **Multimodal Forensic Perception:** Gemini multimodal vision classifies African transit realities (Boda Bodas, helmets, cargo, modified plates), synchronizes regional hotlist meshes, and enables sub-600ms natural-language FreeForm evidence queries. |
| **3. Category Impact** | Protects 200,000+ African gated communities, SACCO stages, and commercial logistics hubs that cannot afford $5,000+ imported Western systems. |

---

## 3. Master Hardware Wiring & Pinout Guide

### Raspberry Pi Zero 2 W (Active Sentry Platform)

```
                              ┌─────────────────────────┐
                              │  Raspberry Pi Zero 2 W  │
                 3.3V Power ──┤ [1]  (3V3)    (5V)  [2] ├── 5V Rail (Amp & Actuator)
     (I2C SDA)       GPIO 2 ──┤ [3]  (GPIO2)  (5V)  [4] ├── 5V Rail
     (I2C SCL)       GPIO 3 ──┤ [5]  (GPIO3)  (GND) [6] ├── Common GND
                      GPIO 4 ──┤ [7]  (GPIO4)  (TXD) [8] ├── GPIO 14
                  Common GND ──┤ [9]  (GND)    (RXD) [10]├── GPIO 15
 (TCRT5000 Tripwire) GPIO 17 ──┤ [11] (GPIO17) (IO18)[12]├── GPIO 18 (I2S BCLK -> Amp)
                     GPIO 27 ──┤ [13] (GPIO27) (GND) [14]├── Common GND
                     GPIO 22 ──┤ [15] (GPIO22) (IO23)[16]├── GPIO 23
                  3.3V Power ──┤ [17] (3V3)    (IO24)[18]├── GPIO 24 (LCD DC)
      (LCD MOSI)     GPIO 10 ──┤ [19] (MOSI)   (GND) [20]├── Common GND
       (SPI MISO)     GPIO 9 ──┤ [21] (MISO)   (IO25)[22]├── GPIO 25 (LCD RST)
      (LCD SCK)      GPIO 11 ──┤ [23] (SCLK)   (CE0) [24]├── GPIO 8  (LCD CS)
                  Common GND ──┤ [25] (GND)    (CE1) [26]├── GPIO 7
      (I2C ID_EE)      ID_SD ──┤ [27] (ID_SD)  (ID)  [28]├── ID_SC
 (SG90 Actuator)     GPIO 12 ──┤ [29] (GPIO12) (GND) [30]├── Common GND
                     GPIO 13 ──┤ [31] (GPIO13) (GND) [34]├── Common GND
     (I2S LRC/FS)    GPIO 19 ──┤ [35] (GPIO19) (IO16)[36]├── GPIO 16
                     GPIO 26 ──┤ [37] (GPIO26) (IO20)[38]├── GPIO 20
                  Common GND ──┤ [39] (GND)    (IO21)[40]├── GPIO 21 (I2S DIN -> Amp)
                               └─────────────────────────┘
```

#### Pin Mapping Table:
| Peripheral | Pin Name | Connects to Pi Zero 2 W Pin | Interface & Function |
| :--- | :--- | :--- | :--- |
| **RPi AI Camera** | MIPI CSI Ribbon | **CSI Camera Port** | Sony IMX500 Neural DSP |
| **GC9A01 1.28" LCD** | `VCC` / `GND` | **Pin 1** (3.3V) / **Pin 14** (GND) | Visual Deterrence Beacon |
| | `SCL` (Clock) | **Pin 23** (GPIO 11) | SPI0_SCLK |
| | `SDA` (Data) | **Pin 19** (GPIO 10) | SPI0_MOSI |
| | `DC` / `CS` / `RST` | **Pins 18, 24, 22** (GPIO 24, 8, 25) | Control Lines |
| | `BLK` (Backlight) | **Pin 17** (3.3V) | Always-on power |
| **MAX98357A Amp** | `VIN` / `GND` | **Pin 2** (5V) / **Pin 6** (GND) | 3W Acoustic Deterrence |
| | `BCLK` / `LRC` / `DIN`| **Pins 12, 35, 40** (GPIO 18, 19, 21)| I2S Digital Audio Bus |
| **MPU-6500 IMU** | `SDA` / `SCL` | **Pins 3 & 5** (GPIO 2, 3) | I2C Bus (`0x68`) — Anti-tamper |
| **TCRT5000 IR** | `DO` | **Pin 11** (GPIO 17) | Optical Arrival Tripwire |
| **CD4069UBE Logic** | Hex Inverter | Interlock Circuit | Hardware tamper clamp |

---

## 4. Software Repository Structure

```
smartB0t/
├── packages/
│   └── protocol/              # Wire framing & Zod schemas (threatLevel, deterrence, fingerprints)
├── apps/
│   ├── backend/               # Google Cloud Run Broker (Gemini Multimodal Live Bridge)
│   │   ├── src/               # gemini.ts, session.ts, bridge.ts, cost-guard.ts, latency.ts
│   │   ├── scripts/soak-test.ts # 30-min automated soak test with fault injection
│   │   └── Dockerfile, deploy.sh
│   ├── playground/
│   │   └── pixel-mock/        # Browser Sentry Intelligence Portal (Vite + Web Audio)
│   └── pi-client/             # Raspberry Pi Zero 2 Native Client
│       ├── test_hardware.py   # One-command smoke test (I2C scan + GC9A01 sentry beacon)
│       └── robot.py           # Live WebSocket client streaming Camera/Mic to Gemini
├── PROTOCOL.md                # Frozen wire specification (v1)
├── BOMASENTRY_MASTER_SPECIFICATION.md # Master project spec, GTM, and XPRIZE narrative
└── IMPLEMENTATION_PLAN.md     # Architecture decisions & cost caps
```

---

## 5. XPRIZE Submission Checklist & Script

### 🎬 3-Minute Demo Video Script
* **0:00 – 0:30 (The Pitch):** "This is BomaSafety — the $110 decentralized AI public safety network eliminating community and transit crime across Africa. Powered by Google Gemini Multimodal Live, it captures vehicle fingerprints and stops transit crime without expensive infrastructure."
* **0:30 – 1:30 (Live Physical Demo):**
  1. Present the Raspberry Pi Zero 2 W + Sony IMX500 AI Camera + GC9A01 display + MAX98357A speaker.
  2. Hold up verified resident plate `KDA 482B` $\rightarrow$ Gemini clears vehicle, LCD glows green beacon.
  3. Hold up suspect Boda `KMDF 892Z` (Red Boxer, gas cylinder) $\rightarrow$ Gemini flags community hotlist match, GC9A01 flashes red alert strobe, MAX98357A speaks verbal warning, and WhatsApp incident alert fires instantly!
* **1:30 – 2:15 (FreeForm™ Crime Search & Latency):** Query: *"Show all motorbikes carrying gas cylinders between 8 AM and 12 PM."* Show sub-600ms latency metrics HUD.
* **2:15 – 3:00 (Business Model & Scaling):** Package A ($0 CapEx, KES 6,500/mo via M-Pesa) and expansion roadmap across East Africa.

### 📝 Devpost Form Fields
* **Title:** BomaSafety — Africa's Vision-Language AI Public Safety Network
* **GitHub Repository:** `https://github.com/bobybarack/smartB0t`
* **Google Cloud Products:** Cloud Run, Gemini 2.5 Multimodal Live API, Cloud Logging, Secret Manager
* **Category:** Small Business Services
