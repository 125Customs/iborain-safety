# 🤖 SmartB0t (Pixel Bot) — Master Project & Submission Report

**Repository:** [https://github.com/bobybarack/smartB0t](https://github.com/bobybarack/smartB0t)  
**Local Monorepo Path:** [`/Users/radebe49/smartB0t`](file:///Users/radebe49/smartB0t)  
**Competition Target:** [Build with Gemini XPRIZE — Devpost ($2,000,000)](https://xprize.devpost.com/)  
**Submission Category:** **Small Business Services**  
**Submission Deadline:** August 17, 2026 @ 1:00 PM PDT

---

## 1. Executive Summary & Value Proposition

**SmartB0t Dispatch** is a physical autonomous micro-courier designed for small businesses (cafés, retail stores, repair workshops, and medical clinics). Powered by the **Google Gemini Multimodal Live API** on Cloud Run and driven by an on-device camera and audio pipeline, SmartB0t replaces expensive manual labor for indoor transport, order dispatch, and physical customer interaction.

```
┌────────────────────────────────────────────────────────┐
│               SMARTB0T CLOUD BRAIN                    │
│      Google Cloud Run ↔ Gemini Multimodal Live API     │
└──────────────────────────▲─────────────────────────────┘
                           │ WebSocket (Protocol v1)
                           │ • AudioIn (16kHz PCM)
                           │ • Jpeg (Vision diff < 1fps)
                           │ • AudioOut (24kHz Native Voice)
                           │ • JSON Control {expression, action}
┌──────────────────────────▼─────────────────────────────┐
│             PHYSICAL ROBOT HARDWARE                    │
│  • Raspberry Pi Zero 2 W + Sony IMX500 AI Camera       │
│  • GC9A01 1.28" Round LCD (Animated Eyes)              │
│  • MAX98357A I2S DAC + iPhone XR 3W Speaker            │
│  • 2x SG90 Continuous Servos (Gated by CD4069 Safety)  │
│  • 3D Printed Rover Chassis + Trailer Payload Box      │
└────────────────────────────────────────────────────────┘
```

---

## 2. XPRIZE Alignment & Judging Strategy

| Judging Pillar (Stage 2) | How SmartB0t Wins |
| :--- | :--- |
| **1. Business Viability & Revenue** | **High-Margin B2B SaaS:** $299 hardware purchase + $49/mo Gemini Dispatch subscription. Demonstrates tangible ROI by saving small businesses $800+/mo in runner labor. |
| **2. AI-Native Operations** | **Full Physical Agency:** Gemini multimodal vision processes the environment live, speaks with natural low-latency voice (<800ms), and drives physical locomotion and eye expressions via structured tool calls. |
| **3. Category Impact** | Democratizes autonomous robotics for local main-street businesses that cannot afford $10,000+ commercial warehouse AGVs. |

### 3D Shell Selection: `robo+trailer.3mf` (Cargo / Micro-Delivery Rover)
* **Model Path:** [`~/Desktop/so 3d print this/robo+trailer.3mf`](file:///Users/radebe49/Desktop/so%203d%20print%20this/robo+trailer.3mf)
* **Why Selected:** Physical payload capability (carrying coffee, parts, medicine) proves commercial utility to judges over a desk novelty toy.

---

## 3. Master Hardware Wiring & Pinout Guide

### A. Raspberry Pi Zero 2 W (Current Active Platform)

```
                              ┌─────────────────────────┐
                              │  Raspberry Pi Zero 2 W  │
                 3.3V Power ──┤ [1]  (3V3)    (5V)  [2] ├── 5V Rail (Servos & Amp)
     (I2C SDA)       GPIO 2 ──┤ [3]  (GPIO2)  (5V)  [4] ├── 5V Rail
     (I2C SCL)       GPIO 3 ──┤ [5]  (GPIO3)  (GND) [6] ├── Common GND
                     GPIO 4 ──┤ [7]  (GPIO4)  (TXD) [8] ├── GPIO 14
                 Common GND ──┤ [9]  (GND)    (RXD) [10]├── GPIO 15
                    GPIO 17 ──┤ [11] (GPIO17) (IO18)[12]├── GPIO 18 (I2S BCLK -> Amp)
                    GPIO 27 ──┤ [13] (GPIO27) (GND) [14]├── Common GND
                    GPIO 22 ──┤ [15] (GPIO22) (IO23)[16]├── GPIO 23
                 3.3V Power ──┤ [17] (3V3)    (IO24)[18]├── GPIO 24 (LCD DC)
     (LCD MOSI)     GPIO 10 ──┤ [19] (MOSI)   (GND) [20]├── Common GND
      (SPI MISO)     GPIO 9 ──┤ [21] (MISO)   (IO25)[22]├── GPIO 25 (LCD RST)
     (LCD SCK)      GPIO 11 ──┤ [23] (SCLK)   (CE0) [24]├── GPIO 8  (LCD CS)
                 Common GND ──┤ [25] (GND)    (CE1) [26]├── GPIO 7
     (I2C ID_EE)      ID_SD ──┤ [27] (ID_SD)  (ID)  [28]├── ID_SC
     (Left Servo)   GPIO 12 ──┤ [29] (GPIO12) (GND) [30]├── Common GND
     (Right Servo)  GPIO 13 ──┤ [31] (GPIO13) (GND) [34]├── Common GND
    (I2S LRC/FS)    GPIO 19 ──┤ [35] (GPIO19) (IO16)[36]├── GPIO 16
                    GPIO 26 ──┤ [37] (GPIO26) (IO20)[38]├── GPIO 20
                 Common GND ──┤ [39] (GND)    (IO21)[40]├── GPIO 21 (I2S DIN -> Amp)
                              └─────────────────────────┘
```

#### Pin Mapping Table:
| Peripheral | Pin Name | Connects to Pi Zero 2 W Pin | Interface |
| :--- | :--- | :--- | :--- |
| **RPi AI Camera** | MIPI CSI Ribbon | **CSI Camera Port** | Sony IMX500 |
| **GC9A01 1.28" LCD** | `VCC` / `GND` | **Pin 1** (3.3V) / **Pin 14** (GND) | Power |
| | `SCL` (Clock) | **Pin 23** (GPIO 11) | SPI0_SCLK |
| | `SDA` (Data) | **Pin 19** (GPIO 10) | SPI0_MOSI |
| | `DC` (Command) | **Pin 18** (GPIO 24) | GPIO |
| | `CS` (Select) | **Pin 24** (GPIO 8) | SPI0_CE0 |
| | `RST` (Reset) | **Pin 22** (GPIO 25) | GPIO |
| | `BLK` (Backlight) | **Pin 17** (3.3V) | Power |
| **MAX98357A Amp** | `VIN` / `GND` | **Pin 2** (5V) / **Pin 6** (GND) | Power (5V Rail) |
| | `BCLK` | **Pin 12** (GPIO 18) | PCM_CLK |
| | `LRC` / `WSEL` | **Pin 35** (GPIO 19) | PCM_FS |
| | `DIN` | **Pin 40** (GPIO 21) | PCM_DOUT |
| **Sensors (Shared I2C)**| `SDA` | **Pin 3** (GPIO 2) | I2C1_SDA (`0x29` ToF & `0x68` IMU) |
| | `SCL` | **Pin 5** (GPIO 3) | I2C1_SCL |
| **SG90 Servos (360°)** | `Signal L / R` | **Pins 29 & 31** (GPIO 12/13) | PWM via CD4069 Cut-Off Loop |
| | `VCC` / `GND` | **5V External Rail** + 470µF Cap | Common Ground |

---

### B. Hardware Cliff Safety Loop (CD4069UBE + TCRT5000)
> **Safety Rule:** Software is NEVER in the safety-critical path. When the robot reaches a table edge, the downward-facing TCRT5000 IR reflection drops. The CD4069 NOT-gate immediately clamps the servo PWM lines to 0V with **0ms latency**, stopping forward motion physically.

---

## 4. Software Repository Structure

```
smartB0t/
├── packages/
│   └── protocol/              # Wire framing & Zod schemas (AudioIn, Jpeg, AudioOut, Control)
├── apps/
│   ├── backend/               # Google Cloud Run Broker (Gemini Multimodal Live Bridge)
│   │   ├── src/               # gemini.ts, session.ts, bridge.ts, cost-guard.ts, latency.ts
│   │   ├── scripts/soak-test.ts # 30-min automated soak test with fault injection
│   │   └── Dockerfile, deploy.sh
│   ├── playground/
│   │   └── pixel-mock/        # Browser hardware simulator (Vite + Web Audio)
│   └── pi-client/             # Raspberry Pi Zero 2 Native Client
│       ├── test_hardware.py   # One-command smoke test (I2C scan + GC9A01 animated eyes)
│       └── robot.py           # Live WebSocket client streaming Camera/Mic to Gemini
├── PROTOCOL.md                # Frozen wire specification (v1)
└── IMPLEMENTATION_PLAN.md     # Architecture decisions & cost caps
```

---

## 5. XPRIZE Submission Checklist & Script

### 🎬 2-Minute Demo Video Script
* **0:00 – 0:30 (The Pitch):** "This is SmartB0t Dispatch — the $40 autonomous AI courier transforming small business operations. Powered by Google Gemini Multimodal Live, it delivers indoor cargo without expensive infrastructure."
* **0:30 – 1:30 (Live Physical Demo):** 
  1. Show item placed into the 3D-printed trailer.
  2. Speak: *"SmartB0t, take these parts to station 2."*
  3. Show Gemini replying in real-time, animated eyes reacting on the GC9A01 LCD, and the rover driving forward.
* **1:30 – 2:00 (Business Model & Google Cloud):** Show the Cloud Run architecture, sub-800ms latency metrics HUD, and the $49/mo SaaS subscription model.

### 📝 Devpost Form Fields
* **Title:** SmartB0t — Autonomous Gemini Micro-Carrier for Small Business
* **GitHub Repository:** `https://github.com/bobybarack/smartB0t`
* **Google Cloud Product:** Cloud Run, Gemini 2.5 Multimodal Live API, Cloud Logging, Secret Manager
* **Category:** Small Business Services
