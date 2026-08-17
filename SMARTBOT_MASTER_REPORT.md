# 🛡️ Iborain Safety — Master Project & Submission Report

**Repository:** [https://github.com/bobybarack/smartB0t](https://github.com/bobybarack/smartB0t)  
**Local Monorepo Path:** [`/Users/radebe49/smartB0t`](file:///Users/radebe49/smartB0t)  
**Competition Target:** [Build with Gemini XPRIZE — Devpost ($2,000,000)](https://xprize.devpost.com/)  
**Submission Category:** **Entrepreneurship & Job Creation** (and Small Business Services)  
**Submission Deadline:** August 17, 2026 @ 1:00 PM PDT  

---

## 1. Executive Summary & Value Proposition

**Iborain Safety** is a decentralized Vision-Language AI public safety and crime elimination network. Born in Nairobi, Iborain reverses the narrative on urban security. Powered by **Google Gemini 3.7 Flash & Live** on Google Cloud Run and edge sentry hardware (Raspberry Pi Zero 2 W + Sony IMX500 AI Camera), Iborain Safety captures multimodal African transit fingerprints, detects community crime hotlist matches in real time, executes autonomous acoustic and visual deterrence, and provides natural-language FreeForm™ crime investigation for security teams and detectives.

```
┌────────────────────────────────────────────────────────┐
│               IBORAIN SAFETY CLOUD BRAIN               │
│       Google Cloud Run ↔ Gemini 3.7 Flash / Live       │
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

| Judging Pillar (Stage 2) | How Iborain Safety Wins |
| :--- | :--- |
| **1. Business Viability & Revenue** | **High-Margin Zero-CapEx SaaS:** Free hardware installation + KES 6,500/mo ($49/mo) community safety subscription billed via automated M-Pesa STK Push. 2.2-month installer payback, 51x LTV/CAC. |
| **2. AI-Native Operations** | **Multimodal Forensic Perception:** Gemini multimodal vision classifies African transit realities (Boda Bodas, helmets, cargo, modified plates), synchronizes regional hotlist meshes, and enables sub-600ms natural-language FreeForm evidence queries. |
| **3. Category Impact (Job Creation)** | Creates the **BomaTech Installer Network**, training youth and informal technicians (*Jua Kali*) to franchise assembly, mounting, and maintenance with a 75-day hardware payback. |

---

## 3. Master Hardware Wiring & Pinout Guide (Raspberry Pi Zero 2 W)

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

---

## 4. Software Repository Structure

```
smartB0t/
├── packages/
│   └── protocol/              # Wire framing & Zod schemas (threatLevel, deterrence, fingerprints)
├── apps/
│   ├── backend/               # Google Cloud Run Broker (Gemini 3.7 Flash & Live Bridge)
│   │   ├── src/               # gemini.ts, session.ts, bridge.ts, cost-guard.ts, latency.ts
│   │   ├── scripts/soak-test.ts # 30-min automated soak test with fault injection
│   │   └── Dockerfile, deploy.sh
│   ├── playground/
│   │   └── pixel-mock/        # Browser Sentry Intelligence Portal (Vite + Web Audio)
│   └── pi-client/             # Raspberry Pi Zero 2 Native Client
│       ├── test_hardware.py   # One-command smoke test (I2C scan + GC9A01 sentry beacon)
│       └── robot.py           # Live WebSocket client streaming Camera/Mic to Gemini
├── PROTOCOL.md                # Frozen wire specification (v1)
├── IBORAIN_MASTER_SPECIFICATION.md # Master project spec, GTM, and XPRIZE narrative
└── IMPLEMENTATION_PLAN.md     # Architecture decisions & cost caps
```

---

## 5. XPRIZE Submission Fields

* **Title:** Iborain Safety: The Community Public Safety Platform
* **GitHub Repository:** `https://github.com/bobybarack/smartB0t`
* **Google Cloud Products:** Cloud Run, Gemini 3.7 Flash & Multimodal Live API, Cloud Logging, Secret Manager
* **Category:** Entrepreneurship & Job Creation (and Small Business Services)
