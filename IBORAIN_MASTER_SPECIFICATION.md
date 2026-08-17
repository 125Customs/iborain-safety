# 🛡️ Iborain Safety — Master Project & Submission Specification

**Project Name:** Iborain Safety: The Community Public Safety Platform  
**Target Category:** **Entrepreneurship & Job Creation** (also Small Business Services)  
**Hackathon Target:** [Build with Gemini XPRIZE — Devpost ($2,000,000)](https://xprize.devpost.com/)  
**Submission Deadline:** August 17, 2026 @ 1:00 PM PDT  
**Hardware Fabrication Hub:** ChipuRobo Workshop & STEM Robotics Lab (Nairobi, Kenya)  

---

## 1. Executive Summary & Problem Framing

### The Monopoly That Failed Africa:
In the United States, **Flock Safety** built a $4 Billion public safety monopoly by leasing solar-powered automated license plate recognition (ALPR) cameras to 12,000+ communities to eliminate property crime.

However, Flock’s architecture costs **$3,000 to $5,500+ per camera/year** and fails completely across Africa:
1. **Cost Exclusion:** It is financially unattainable for 99% of African neighborhoods, schools, and transport hubs.
2. **Transit Reality Blindspot:** Rigid OCR models fail on African transit realities—unregistered **Boda Bodas** (motorcycles), missing/muddy plates, modified **Toyota Proboxes**, and informal cargo.
3. **Siloed Defenses:** When a burglary strikes in one estate, neighboring communities receive zero warning because they share zero threat intelligence.
4. **The Evidence Black Hole:** Over 70% of violent and property crimes rely on getaway vehicles and motorbikes. When crime happens, detectives face an evidence void with zero searchable leads.

### The Solution: Iborain Safety
Born in Nairobi, **Iborain Safety** reverses the narrative on urban security. Powered by a **$110 production hardware BOM** running on a **Raspberry Pi Zero 2 W** paired with the **Sony IMX500 AI Camera** and **Google Gemini 3.7 Flash & Live on Google Cloud Run**, Iborain Safety blankets communities in a low-cost, solar-ready safety grid. It automatically captures multimodal vehicle and Boda fingerprints, detects regional crime hotlist matches in real time, executes autonomous acoustic and visual deterrence, and provides natural-language FreeForm™ crime investigation for detectives and security committees.

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   IBORAIN SAFETY CLOUD BRAIN                                     │
│                     Google Cloud Run ↔ Gemini 3.7 Flash / Multimodal Live                       │
│           • Sub-600ms WebSocket Inference & Session Resumption (2-Min Cap Bypass)                │
│           • African Transit Forensics & Inter-Community Crime Hotlist Mesh                       │
│           • FreeForm™ Natural Language Multimodal Crime Investigation Engine                     │
└──────────────────────────────────────────────▲───────────────────────────────────────────────────┘
                                               │ WebSocket (Protocol v1)
                                               │ • 16kHz PCM Sentry Audio Stream
                                               │ • 1fps JPEG Vision Diffs (IMX500 HDR)
                                               │ • JSON Structured Threat Payload
┌──────────────────────────────────────────────▼───────────────────────────────────────────────────┐
│                                  TACTICAL SENTRY UNIT                                            │
│  • Edge Compute: Raspberry Pi Zero 2 W (Quad-Core 64-bit ARM, 5V/0.5A Ultra-Low Draw)            │
│  • Vision Sensor: Raspberry Pi AI Camera (Sony IMX500 Neural DSP)                                │
│  • Visual Deterrence: GC9A01 1.28" Round LCD (Active Sentry Strobe & Radar Beacon)               │
│  • Acoustic Deterrence: MAX98357A I2S 3W Class D DAC Amplifier + Speaker                        │
│  • Anti-Tamper & Anti-Theft: MPU-6500 6-Axis Gyroscope/Accelerometer (I2C 0x68)                  │
│  • Optical Arrival Tripwire: TCRT5000 Infrared Reflective Sensor (GPIO 17)                       │
│  • Hardware Tamper Clamp: CD4069UBE CMOS Hex Inverter Logic Gate                                │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Reverse-Engineering: Flock Safety vs. Iborain Safety

| Feature / Dimension | 🦅 Flock Safety (US Market) | 🛡️ Iborain Safety (African Market) |
| :--- | :--- | :--- |
| **Annual Cost per Camera** | **$3,000 – $5,500+ USD / year** | **$49 / month ($588 USD / year)** |
| **Hardware BOM Cost** | Proprietary Western HW ($1,500+) | **$110 USD (KES 14,200)** via ChipuRobo Lab |
| **Edge Hardware Platform** | Custom Industrial Board (High Power) | **Raspberry Pi Zero 2 W + Sony IMX500 AI Cam** |
| **Vision Intelligence** | Rigid LPR / Plate OCR | **African Transit Fingerprinting™ (Gemini 3.7)** |
| **Boda Boda & Cargo Profiling**| ❌ None (US Vehicle biased) | ✅ Full (Fuel tanks, helmets, 13kg gas cylinders, sacks) |
| **Muddy / Obscured Plates** | ❌ Fails / Zero Detection | ✅ Semantic Context Reasoning |
| **Threat Intelligence Mesh** | Centralized US Police Database | **Decentralized Inter-Community Hotlist Grid** |
| **Resident Communication** | Email / Proprietary App | **Real-Time 2-Way WhatsApp Security Mesh** |
| **Billing & Payments** | Western Annual Net-30 Invoices | **Automated Monthly M-Pesa STK Push (Daraja API)** |
| **Job Creation Engine** | Silicon Valley Corporate Techs | **The BomaTech Installer Network (Jua Kali Youth)** |

---

## 3. The 3 Pillars of Iborain Safety

### Pillar 1: African Transit Fingerprinting™ (Beyond Basic OCR)
Powered by Gemini 3.7 Flash, Iborain extracts the **complete physical fingerprint**:
* **License Plate Text & Mud Delta**: Reads Kenyan plate formats (`KDA 482B`, `KMDF 892Z`, or flags `UNPLATED`).
* **Vehicle Make, Model & Customizations**: Identifies modifications (e.g. *"White Toyota Probox, tinted rear windows, heavy-duty roof rack, right rear bumper dent"*).
* **Boda Boda Classification & Cargo**: Identifies motorbike models (*Boxer 150, TVS King, Bajaj*), fuel tank colors, rider reflector jacket color, helmet compliance, and distinctive cargo (*13kg gas cylinders, courier backpacks, sacks*).

### Pillar 2: Decentralized Inter-Estate Hotlist & Threat Mesh
* When an incident occurs in one estate, a high-priority threat fingerprint is published to the regional mesh.
* Every Iborain unit within a 10km radius is synchronized immediately.
* When that vehicle passes any connected checkpoint, Iborain triggers:
  1. **Instant WhatsApp Alert** to local security patrols with photo proof.
  2. **Active Edge Deterrence**: GC9A01 LCD flashes Red/Blue police strobe; MAX98357A speaker delivers verbal warning (*"Warning: Vehicle flagged on community crime watch"*).

### Pillar 3: FreeForm™ Natural Language Crime Investigation Search
Detectives and estate chairmen search forensic records in plain natural language:
> *"Show all motorbikes carrying gas cylinders entering Syokimau Court 4 between 1:00 AM and 4:30 AM."*  
> *"Find any white Toyota Probox with a dented bumper and no front plate seen in the last 48 hours."*

---

## 4. Master Hardware Pinout & Wiring (Raspberry Pi Zero 2 W)

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

## 5. Commercial Go-to-Market & Financial P&L

### Package A: The Zero-CapEx Safety Lease
* **Upfront Hardware Cost to Community:** **KES 0 ($0 CapEx)**
* **Setup & Network Calibration Fee:** **KES 3,500 ($27 USD)**
* **Monthly SaaS Subscription:** **KES 6,500 / month ($49 USD)** per gate, billed via **M-Pesa STK Push**.

### Unit Economics:
* **Hardware BOM Cost:** KES 14,200 ($110 USD)
* **Monthly Operating Cost (Cloud/IoT):** KES 700 ($5 USD)
* **Monthly Net Cash Flow per Gate:** KES 5,800 ($44 USD)
* **Payback Period:** **2.44 months (74 days)**
* **Year 1 Net Operating Income (150 Units):** **$86,400 USD (78.1% Gross Margin)**
* **LTV / CAC Ratio:** **50.4x** ($1,764 LTV vs. $35 CAC)
