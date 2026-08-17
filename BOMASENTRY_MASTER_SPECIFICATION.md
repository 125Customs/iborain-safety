# 🛡️ BomaSentry — Master Project & Submission Specification
### *Africa’s First Vision-Language AI Sentry & Autonomous Gatekeeper*

**Repository:** [https://github.com/bobybarack/smartB0t](https://github.com/bobybarack/smartB0t)  
**Target Competition:** [Build with Gemini XPRIZE — Devpost ($2,000,000 Cash Prizes)](https://xprize.devpost.com/)  
**Submission Category:** **Small Business Services**  
**Submission Deadline:** August 17, 2026 @ 1:00 PM PDT  

---

## 1. Executive Summary & The African Opportunity

In the United States, **Flock Safety** built a multi-billion dollar public safety monopoly by leasing solar-powered license plate recognition (ALPR) cameras to 12,000+ communities and 7,000+ police departments. However, Flock’s architecture costs **$3,000 – $5,500+ per camera/year** and fails completely in Africa because:
1. It is too expensive for African communities.
2. It cannot categorize African transit realities (unregistered **Boda Bodas**, delivery cargo, **Matatus**, modified **Proboxes**, missing/muddy plates).
3. It lacks two-way resident interaction through Africa's primary digital channel: **WhatsApp**.

**BomaSentry** is the next-generation, Flock-style multimodal intelligence platform built specifically for Africa. Powered by a **$32 hardware Bill of Materials (BOM)** running on a **Raspberry Pi Zero 2 W** and the **Google Gemini Multimodal Live API on Cloud Run**, BomaSentry replaces manual paper logbooks with automated barrier actuation, real-time WhatsApp visitor approvals, and natural-language "FreeForm" security search for gated communities, schools, SACCO stages, and hospitals.

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   BOMASENTRY CLOUD BRAIN                                        │
│                           Google Cloud Run ↔ Gemini Multimodal Live                             │
│       • Vision-Language Scene Fingerprinting (Vehicle make, color, Boda traits, cargo)          │
│       • FreeForm Natural Language Security Search & Incident Narrative Generation               │
│       • WhatsApp Business API Webhook Integration (Resident 2-Way Clearance)                    │
└──────────────────────────────────────────────▲──────────────────────────────────────────────────┘
                                               │ WebSocket (Protocol v1)
                                               │ • 1fps JPEG Vision Diffs (IMX500 HDR Frame)
                                               │ • JSON Structured Action Payload
┌──────────────────────────────────────────────▼──────────────────────────────────────────────────┐
│                                 EDGE HARDWARE SENTRY UNIT                                       │
│  • Compute: Raspberry Pi Zero 2 W (Quad-Core 64-bit ARM, 512MB RAM, 5V/0.5A)                   │
│  • Vision: Sony IMX500 AI Camera (On-sensor neural motion trigger + hardware HDR)               │
│  • Visual Interface: GC9A01 1.28" Round RGB TFT LCD (Animated status & clearance eyes)          │
│  • Physical Actuation: SG90 Micro Servo (90° Boom Barrier Gate Arm)                            │
│  • Presence & Safety: TCRT5000 Infrared Reflective Proximity Sensor (Anti-Crush Cutoff)        │
│  • Anti-Tamper: MPU6500 6-Axis Accelerometer (Anti-theft & vibration alarm)                    │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Technical Reverse-Engineering: Flock Safety vs. BomaSentry

| Feature / Dimension | 🦅 Flock Safety (US Market) | 🛡️ BomaSentry (African Market) |
| :--- | :--- | :--- |
| **Year 1 Cost / Gate** | **$3,000 – $5,500 USD** | **$49 / month ($65 BOM hardware lease)** |
| **Edge Hardware** | Custom proprietary solar-cellular pole camera | **Raspberry Pi Zero 2 W + Sony IMX500 AI Camera** |
| **Machine Vision Engine** | Rigid OCR + Proprietary Vehicle Fingerprint™ | **Gemini Multimodal Live (Vision-Language Model)** |
| **African Transit Support** | None (Fails on missing front plates & Bodas) | **Full Boda Boda classification (helmets, cargo, jackets)** |
| **User & Resident Interface** | Web dispatch portal & email alerts | **Interactive 2-Way WhatsApp Bot (Twilio/Meta)** |
| **Physical Agency** | Passive camera only (No barrier control) | **Active barrier control (SG90 Servo / 12V Relay)** |
| **Privacy & Compliance** | 7-day auto-purge, Zero Facial Recognition | **Zero Facial Recognition, 7-day auto-purge (Kenya DPA 2019)** |

---

## 3. The 3 Product Tiers & Business Model

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    BOMASENTRY PRODUCT TIERS                                     │
├─────────────────────────┬───────────────────────────────┬───────────────────────────────────────┤
│ Tier 1: LITE            │ Tier 2: PRO (Core MVP)        │ Tier 3: ENTERPRISE                    │
│ (Courts & Small Gates)  │ (Gated Estates & SACCOs)      │ (Malls, Hospitals, County Borders)   │
├─────────────────────────┼───────────────────────────────┼───────────────────────────────────────┤
│ • Pi Zero 2 W           │ • Pi Zero 2 W                 │ • Raspberry Pi 5                      │
│ • OV5647 Camera         │ • Sony IMX500 AI Camera       │ • Dual IMX500 (Entry & Exit Lanes)    │
│ • WhatsApp API Webhook  │ • GC9A01 LCD + SG90 Servo     │ • 4G LTE Cellular + Industrial Relay  │
│ • Cloud Gemini API      │ • TCRT5000 IR + WhatsApp API  │ • Local SQLite Cache + Multi-Lane LPR │
│                         │ • 10W Solar + Battery Pack    │                                       │
│ BOM: KSh 3,200 ($25)    │ BOM: KSh 8,500 ($65)          │ BOM: KSh 22,000 ($170)                │
│ Lease: $19 / month      │ Lease: $49 / month            │ Lease: $129 / month                   │
└─────────────────────────┴───────────────────────────────┴───────────────────────────────────────┘
```

---

## 4. Hardware Pinout & Wiring Specification

```
                              ┌─────────────────────────┐
                              │  Raspberry Pi Zero 2 W  │
                 3.3V Power ──┤ [1]  (3V3)    (5V)  [2] ├── 5V Rail (Servos & Amp)
     (I2C SDA)       GPIO 2 ──┤ [3]  (GPIO2)  (5V)  [4] ├── 5V Rail
     (I2C SCL)       GPIO 3 ──┤ [5]  (GPIO3)  (GND) [6] ├── Common GND
                      GPIO 4 ──┤ [7]  (GPIO4)  (TXD) [8] ├── GPIO 14
                  Common GND ──┤ [9]  (GND)    (RXD) [10]├── GPIO 15
 (TCRT5000 IR In)    GPIO 17 ──┤ [11] (GPIO17) (IO18)[12]├── GPIO 18 (I2S BCLK -> Amp)
                     GPIO 27 ──┤ [13] (GPIO27) (GND) [14]├── Common GND
                     GPIO 22 ──┤ [15] (GPIO22) (IO23)[16]├── GPIO 23
                  3.3V Power ──┤ [17] (3V3)    (IO24)[18]├── GPIO 24 (LCD DC)
      (LCD MOSI)     GPIO 10 ──┤ [19] (MOSI)   (GND) [20]├── Common GND
       (SPI MISO)     GPIO 9 ──┤ [21] (MISO)   (IO25)[22]├── GPIO 25 (LCD RST)
      (LCD SCK)      GPIO 11 ──┤ [23] (SCLK)   (CE0) [24]├── GPIO 8  (LCD CS)
                  Common GND ──┤ [25] (GND)    (CE1) [26]├── GPIO 7
      (I2C ID_EE)      ID_SD ──┤ [27] (ID_SD)  (ID)  [28]├── ID_SC
     (SG90 Servo)   GPIO 12 ──┤ [29] (GPIO12) (GND) [30]├── Common GND
                     GPIO 13 ──┤ [31] (GPIO13) (GND) [34]├── Common GND
     (I2S LRC/FS)    GPIO 19 ──┤ [35] (GPIO19) (IO16)[36]├── GPIO 16
                     GPIO 26 ──┤ [37] (GPIO26) (IO20)[38]├── GPIO 20
                  Common GND ──┤ [39] (GND)    (IO21)[40]├── GPIO 21 (I2S DIN -> Amp)
                               └─────────────────────────┘
```

---

## 5. Vision-Language Workflow & FreeForm Querying

### A. Live Vehicle Ingestion & WhatsApp Trigger
1. **Approach**: A delivery Boda Boda (`KMDF 892Z`) carrying a 13kg gas cylinder approaches the gate.
2. **Edge Trigger**: Sony IMX500 detects motion; Pi Zero 2 W sends a single frame diff to Cloud Run.
3. **Gemini Semantic Reasoning**:
   * Extracts plate: `KMDF 892Z`.
   * Identifies traits: `Red Boxer Motorcycle`, `Rider in yellow reflector jacket`, `Cargo: 13kg Blue Gas Cylinder`.
4. **WhatsApp Push to Resident (House 42)**:
   > *"🛡️ BomaSentry Alert: A delivery Boda (KMDF 892Z) carrying a gas cylinder has arrived for House 42. Reply '1' to OPEN GATE for 5 minutes or '2' to DENY."*
5. **Clearance**: Resident replies `1` $\rightarrow$ Gemini executes tool `open_barrier()` $\rightarrow$ SG90 servo lifts gate $\rightarrow$ LCD turns green $\rightarrow$ Event logged to audit table.

### B. Natural Language FreeForm Search (Estate Dashboard)
* **Query**: *"Show me all motorbikes carrying cargo that entered through North Gate between 8 AM and 12 PM."*
* **Gemini Response**: *"Found 2 matches: 1) KMDF 892Z (Red Boxer, 13kg gas cylinder) at 09:14 AM. 2) KMEB 104A (Black TVS, 2 jerricans) at 11:02 AM."*

---

## 6. Official XPRIZE Submission Narrative (500–1000 Words)

### Project Title: BomaSentry — Africa's Vision-Language AI Gatekeeper

#### 1. What Problem Does BomaSentry Solve?
Across Sub-Saharan Africa, over 200,000 gated residential communities, commercial parks, SACCO stages, and hospitals rely on underpaid physical security guards manually writing vehicle registration numbers into paper logbooks. This century-old practice creates massive security vulnerabilities: stolen vehicles with cloned plates pass through undetected, phone-snatching boda bodas enter without accountability, and entry queues back up into traffic. Meanwhile, imported Western systems like Flock Safety cost upwards of $5,000 per camera, pricing out 99% of African communities while failing to recognize African vehicle types.

#### 2. What Does the AI Do vs. What Do Humans Do?
BomaSentry transforms gate security through an AI-native operational model:
* **What Gemini Multimodal AI Does**: The AI operates 24/7 as the perceptual and decision-making sentry. Powered by the Gemini Multimodal Live API on Google Cloud Run, it analyzes camera frames streamed from a $15 Raspberry Pi Zero 2 W, reading Kenyan license plates, classifying vehicle body types, identifying Boda Boda cargo (gas cylinders, courier bags), detecting rider safety compliance, and executing physical gate barrier actuation. When unverified visitors arrive, the AI autonomously dispatches 2-way approval requests over WhatsApp to residents.
* **What Humans Do**: Estate security guards shift from mundane data entry clerks to dignified rapid-response officers who only handle escalated anomalies flagged by the AI. Residents retain final clearance authority through one-tap WhatsApp confirmations.

#### 3. Jobs and Economic Opportunities Created
Rather than displacing local workers, BomaSentry creates sustainable high-value technical jobs. We are establishing the **BomaTech Installer Network**, training youth from Kenya’s informal *Jua Kali* sector to assemble, install, and maintain solar-powered BomaSentry units across residential estates and commercial centers. By keeping our hardware Bill of Materials under $35, we enable local entrepreneurs to franchise BomaSentry installations with payback in month one.

#### 4. Privacy, Safety & Regulatory Compliance
In strict compliance with the **Kenya Data Protection Act (2019)**, BomaSentry enforces a strict **Zero Facial Recognition** policy. The system captures only vehicle attributes and license plates, and all event data is automatically purged after 7 days unless preserved by authorized community administrators.

---

## 7. Financial Model & P&L Summary (XPRIZE Submission)

| Financial Metric | Year 1 Projection (150 Gates) | Year 2 Projection (1,200 Gates) |
| :--- | :--- | :--- |
| **Active Subscriptions (Tier 2 @ $49/mo)** | $88,200 USD | $705,600 USD |
| **Hardware Lease Revenue (Tier 1/3)** | $22,500 USD | $180,000 USD |
| **Total Annual Revenue** | **$110,700 USD** | **$885,600 USD** |
| **Hardware BOM & Cellular IoT SIM Costs** | ($19,500 USD) | ($144,000 USD) |
| **Google Cloud Run & Gemini API Usage** | ($4,800 USD) | ($38,400 USD) |
| **Gross Margin** | **78.1%** | **79.4%** |
| **Net Operating Income** | **$86,400 USD** | **$703,200 USD** |

---

## 8. Today's 3-Minute Video Demo Blueprint

* **0:00 – 0:30 (The Urgent African Crisis)**: Open with a shot of a Nairobi estate gate. Show the guard struggling with a paper logbook while cars wait. Explain how BomaSentry solves this for $49/mo.
* **0:30 – 1:30 (The Live Hardware Demonstration)**:
  * Camera focuses on the Pi Zero 2 W + Sony IMX500 AI Camera + GC9A01 LCD.
  * Hold up plate `KDA 482B`.
  * Show Gemini identifying the plate, LCD flashing Green ("ACCESS GRANTED"), and the SG90 servo lifting the barrier arm!
  * Hold up `KMDF 892Z` (Boda). Show the simulated WhatsApp push asking for resident clearance.
* **1:30 – 2:15 (Cloud Architecture & Gemini Logs)**:
  * Show screen recording of Google Cloud Run logs running live WebSocket inferences at <600ms latency.
* **2:15 – 3:00 (Business Model & Expansion Vision)**:
  * Present the 3 product tiers, the $32 BOM economics, and the roadmap to secure 5,000+ gates across East Africa.
