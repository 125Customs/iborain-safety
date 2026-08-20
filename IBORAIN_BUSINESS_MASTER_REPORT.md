# 📊 Iborain Safety — Master Commercial & Financial Execution Report
*Private Commercial Blueprint & Investor / Partnership Dossier*

**Company:** Iborain Safety Ltd. (Nairobi, Kenya)  
**Hardware Incubation Partner:** [ChipuRobo STEM Makerspaces](https://chipurobo.com/)  
**Core Model:** Hardware-Enabled B2B SaaS & Installer Micro-Franchise Network  
**Target Market:** Sub-Saharan Africa (Beachhead: Nairobi Metro, Kenya)  
**Currency Standard:** Kenyan Shillings (KES) & US Dollars (USD @ 1 USD = 130 KES)

---

## 1. Executive Summary & Market Sizing

**Iborain Safety** is a decentralized Vision-Language AI public safety and crime elimination network born in Nairobi. Over 70% of urban violent and property crime in Sub-Saharan Africa is transit-borne, carried out using unplated/cloned vehicles and motorcycles (*Boda Bodas*).

Existing Western ALPR systems (Flock Safety at $5,000/camera/year) are cost-prohibitive for 99% of African communities and fail completely on local transit realities (muddy plates, modified Proboxes, informal cargo). Dumb CCTV systems (Hikvision/Dahua) only record passive video without real-time detection.

Iborain delivers **Stealth, Real-Time Crime Elimination starting at $49/month (KES 6,500/mo) with Zero Upfront CapEx**, powered by Google Gemini (Gemini 3.7 Flash & Live API) on Google Cloud Run and streamlined edge sentry hardware fabricated locally at ChipuRobo makerspaces in Nairobi.

---

## 2. The 3 Hardware Tiers: Full Bill of Materials & Manufacturing Specs

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 THE 3 IBORAIN HARDWARE TIERS                                     │
├────────────────────────────────┬────────────────────────────────┬────────────────────────────────┤
│ 🟢 Tier 1: Iborain Lite        │ 🔵 Tier 2: Iborain Tactical    │ 🟣 Tier 3: Iborain Solar Pro   │
│    (High-Velocity Checkpoint)  │    (Neural Transit Sentry)     │    (Off-Grid Corridor Node)    │
├────────────────────────────────┼────────────────────────────────┼────────────────────────────────┤
│ • BOM Cost: $59.50 (KES 7,735) │ • BOM Cost: $135.00 (KES 17.5k)│ • BOM Cost: $235.00 (KES 30.5k)│
│ • Subscription: $49/mo (6.5k)  │ • Subscription: $73/mo (9.5k)  │ • Subscription: $104/mo (13.5k)│
│ • Payback: 39 Days (1.3 mo)    │ • Payback: 43–61 Days (1.4 mo) │ • Payback: 41–75 Days (2.5 mo) │
│ • Power: AC/Grid (5V/2A)       │ • Power: AC / 12V Grid + 4G    │ • Power: 100% Solar + LiFePO4  │
└────────────────────────────────┴────────────────────────────────┴────────────────────────────────┘
```

---

### 🟢 TIER 1: Iborain Lite (The High-Velocity Checkpoint Node)

**Ideal Deployment:** Residential estate barrier gates, school entrances, quiet gated courts (Grid-powered, Wi-Fi or basic 4G).

#### 1. Material & Component Bill of Materials (BOM)

| Subsystem / Part | Technical Specification | Unit Cost (USD) | Unit Cost (KES) | Sourcing / Fabrication |
| :--- | :--- | :---: | :---: | :--- |
| **Compute Board** | Raspberry Pi Zero 2 W (Quad-Core 64-bit ARM) | $25.00 | KES 3,250 | Official RPi Distro / ChipuRobo |
| **Vision Sensor** | Raspberry Pi Camera Module 3 (12MP Sony IMX708 Autofocus/HDR) | $25.00 | KES 3,250 | Camera Supplier |
| **Anti-Tamper Sensor** | MPU-6500 6-Axis Gyro/Accelerometer (I2C 0x68) | $2.00 | KES 260 | ChipuRobo Lab Stock |
| **Optical Tripwire** | TCRT5000 Infrared Reflective Sensor (GPIO 17) | $1.00 | KES 130 | Sensor Importer |
| **Status Indicator** | High-Intensity Dual-Color Green/Red Status LED | $0.50 | KES 65 | Electronics Wholesale |
| **3D Printed Enclosure** | 120g UV-Resistant PETG filament ($2.40) + Machine Time ($0.60) | $3.00 | KES 390 | ChipuRobo 3D Print Farm |
| **Power Supply** | 5V 3A AC/DC Wall Adapter with Surge Protection | $2.00 | KES 260 | Electronics Wholesale |
| **Fasteners & Glands** | Stainless M3 Screws, IP68 PG7 Cable Gland, JST Wire Harness | $1.00 | KES 130 | Local Hardware Sourcing |
| **TOTAL TIER 1 BOM** | **Complete Assembled Iborain Lite Node** | **$59.50** | **KES 7,735** | **100% Fully Built** |

#### 2. Tier 1 Commercial & Monthly Cash Flow Model

$$\begin{aligned}
\text{Upfront Hardware Cost to Customer} &= \text{KES } 0 \text{ (\$0 CapEx)} \\
\text{One-Time Setup \& Network Calibration Fee} &= \text{KES } 3,500 \text{ (\$27.00 USD)} \\
\text{Monthly Recurring Subscription (MRR)} &= \text{KES } 6,500 \text{ / month (\$49.00 USD)} \\
\hline
\text{Less: Google Cloud Run Compute} &= -\text{KES } 260 \text{ (-\$2.00 USD)} \\
\text{Less: Gemini 3.7 Flash API Tokens} &= -\text{KES } 195 \text{ (-\$1.50 USD)} \\
\text{Less: 4G IoT SIM Data (Safaricom/Airtel)} &= -\text{KES } 245 \text{ (-\$1.88 USD)} \\
\hline
\mathbf{\text{Monthly Net Contribution Margin}} &= \mathbf{\text{KES } 5,800 \text{ / month (\$44.62 USD)}} \\
\mathbf{\text{Gross Contribution Margin \%}} &= \mathbf{89.2\%} \\
\mathbf{\text{Capital Payback Period}} &= \frac{\text{KES } 7,735}{\text{KES } 5,800 \text{/mo}} = \mathbf{1.33 \text{ Months (39 Days!)}}
\end{aligned}$$

---

### 🔵 TIER 2: Iborain Tactical (The Neural Transit & SACCO Sentry)

**Ideal Deployment:** Transport SACCO stages, warehouse logistics yards, commercial petrol stations, high-traffic gated communities (Grid-powered or 12V line, 4G LTE).

#### 1. Material & Component Bill of Materials (BOM)

| Subsystem / Part | Technical Specification | Unit Cost (USD) | Unit Cost (KES) | Sourcing / Fabrication |
| :--- | :--- | :---: | :---: | :--- |
| **Compute Board** | Raspberry Pi Zero 2 W (Quad-Core 64-bit ARM) | $25.00 | KES 3,250 | Official RPi Distro / ChipuRobo |
| **Neural AI Camera** | Raspberry Pi AI Camera (12.3MP Sony IMX500 with On-Chip Neural DSP) | $70.00 | KES 9,100 | ChipuRobo Lab Stock |
| **Cellular IoT Modem** | Quectel / Waveshare 4G LTE Cellular HAT + High-Gain Antenna | $24.00 | KES 3,120 | RF / Cellular Importer |
| **Anti-Tamper Sensor** | MPU-6500 6-Axis Gyro/Accelerometer (I2C 0x68) | $2.00 | KES 260 | ChipuRobo Lab Stock |
| **Optical Tripwire** | TCRT5000 Infrared Reflective Sensor (GPIO 17) | $1.00 | KES 130 | Sensor Importer |
| **Status Indicator** | High-Intensity Dual-Color Green/Red Status LED | $0.50 | KES 65 | Electronics Wholesale |
| **3D Printed Enclosure** | 180g PETG with Sunshade Hood ($3.60) + Machine Time ($0.90) | $4.50 | KES 585 | ChipuRobo 3D Print Farm |
| **Power Subsystem** | 12V to 5V 3A DC Buck Converter & Power Line Filter | $3.00 | KES 390 | Electronics Importer |
| **Pole Mounting Bracket**| Stainless Steel Adjustable Pole Clamp & Arm | $3.00 | KES 390 | Local Metal Fabrication |
| **Fasteners & Glands** | Stainless M3 Screws, IP68 PG7 Cable Glands, JST Wire Harness | $2.00 | KES 260 | Local Hardware Sourcing |
| **TOTAL TIER 2 BOM** | **Complete Assembled Iborain Tactical Node** | **$135.00** | **KES 17,550** | **100% Fully Built** |

#### 2. Tier 2 Commercial & Monthly Cash Flow Model

$$\begin{aligned}
\text{Upfront Hardware Cost to Customer} &= \text{KES } 5,000 \text{ (\$38.00 USD)} \\
\text{Monthly Recurring Subscription (MRR)} &= \text{KES } 9,500 \text{ / month (\$73.00 USD)} \\
\hline
\text{Less: Google Cloud Run Compute} &= -\text{KES } 325 \text{ (-\$2.50 USD)} \\
\text{Less: Gemini 3.7 Flash API Tokens} &= -\text{KES } 260 \text{ (-\$2.00 USD)} \\
\text{Less: 4G LTE IoT SIM Data (Safaricom/Airtel)} &= -\text{KES } 365 \text{ (-\$2.80 USD)} \\
\hline
\mathbf{\text{Monthly Net Contribution Margin}} &= \mathbf{\text{KES } 8,550 \text{ / month (\$65.70 USD)}} \\
\mathbf{\text{Gross Contribution Margin \%}} &= \mathbf{90.0\%} \\
\mathbf{\text{Capital Payback Period}} &= \frac{\text{KES } 17,550 - \text{KES } 5,000 \text{ (Upfront)}}{\text{KES } 8,550 \text{/mo}} = \mathbf{1.46 \text{ Months (43 Days)}} \\
&(\text{Without Upfront: } \frac{\text{KES } 17,550}{\text{KES } 8,550} = \mathbf{2.05 \text{ Months / 61 Days}})
\end{aligned}$$

---

### 🟣 TIER 3: Iborain Solar Pro (The Off-Grid Corridor Node — "The Falcon Equivalent")

**Ideal Deployment:** Public street light poles, arterial highway feeder junctions, unpowered municipal avenues (100% Solar Off-Grid, Dual 4G + GPS, 30m Night Vision).

#### 1. Material & Component Bill of Materials (BOM)

| Subsystem / Part | Technical Specification | Unit Cost (USD) | Unit Cost (KES) | Sourcing / Fabrication |
| :--- | :--- | :---: | :---: | :--- |
| **Compute Board** | Raspberry Pi Zero 2 W (Quad-Core 64-bit ARM) | $25.00 | KES 3,250 | Official RPi Distro / ChipuRobo |
| **Neural AI Vision** | Sony IMX500 AI Camera + C/CS Mount Telephoto Optical Zoom Lens | $82.00 | KES 10,660 | Optical / AI Sensor Supplier |
| **Solar Panel** | 30W Monocrystalline Anodized Aluminum Weatherproof Panel | $22.00 | KES 2,860 | Local Solar Wholesaler |
| **Battery Storage** | 12V 12Ah LiFePO4 Battery Pack (>2,500 Cycles, Thermal Grade) | $28.00 | KES 3,640 | Lithium Battery Depot |
| **MPPT Solar Controller** | Intelligent MPPT Solar Charge Controller + 5V/3A DC-DC Buck Stepdown | $10.00 | KES 1,300 | Electronics Importer |
| **Cellular & GPS** | Quectel EC25-E Global 4G LTE HAT + High-Gain Omni Antenna + GPS | $28.00 | KES 3,640 | RF / IoT Telecom |
| **Carrier Dual-SIM** | Dual-SIM IoT Carrier Board (Safaricom / Airtel Auto-Failover) | $2.00 | KES 260 | Telecom Hardware |
| **Night Vision IR Array** | 12V High-Power 850nm Infrared LED Array (30m Night Vision) | $12.00 | KES 1,560 | CCTV Component Wholesaler |
| **Anti-Tamper Sensor** | MPU-6500 6-Axis Gyro/Accelerometer (I2C 0x68) | $2.00 | KES 260 | ChipuRobo Lab Stock |
| **Doppler Radar Sensor** | 10.525GHz Microwave Doppler Radar (15m wide-road detection) | $3.00 | KES 390 | Sensor Importer |
| **Industrial Enclosure** | IP66 Die-Cast Aluminum & Polycarbonate Box with Gore-Tex Vent | $12.00 | KES 1,560 | Industrial Plastics / Metal |
| **Heavy-Duty Mount** | Galvanized Steel Universal Pole-Mount Arm & Stainless Straps | $5.00 | KES 650 | Local Metal Fabrication |
| **Fasteners, Glands & QA**| IP68 Glands, Silicon O-Rings, Wire Harness, ChipuRobo QA | $4.00 | KES 520 | ChipuRobo Makerspace QA |
| **TOTAL TIER 3 BOM** | **Complete Industrial Off-Grid Corridor Sentry** | **$235.00** | **KES 30,550** | **100% Fully Built** |

#### 2. Tier 3 Commercial & Monthly Cash Flow Model

$$\begin{aligned}
\text{One-Time Pole Installation \& Calibration Fee} &= \text{KES } 15,000 \text{ (\$115.00 USD)} \\
\text{Monthly Recurring Subscription (MRR)} &= \text{KES } 13,500 \text{ / month (\$104.00 USD)} \\
\hline
\text{Less: Google Cloud Run Compute} &= -\text{KES } 455 \text{ (-\$3.50 USD)} \\
\text{Less: Gemini 3.7 Flash API Tokens} &= -\text{KES } 390 \text{ (-\$3.00 USD)} \\
\text{Less: Dual-SIM 4G LTE IoT SIM Data} &= -\text{KES } 555 \text{ (-\$4.27 USD)} \\
\hline
\mathbf{\text{Monthly Net Contribution Margin}} &= \mathbf{\text{KES } 12,100 \text{ / month (\$93.08 USD)}} \\
\mathbf{\text{Gross Contribution Margin \%}} &= \mathbf{89.6\%} \\
\mathbf{\text{Capital Payback Period}} &= \frac{\text{KES } 30,550 - \text{KES } 15,000 \text{ (Setup)}}{\text{KES } 12,100 \text{/mo}} = \mathbf{1.28 \text{ Months (38 Days)}} \\
&(\text{Without Setup: } \frac{\text{KES } 30,550}{\text{KES } 12,100} = \mathbf{2.52 \text{ Months / 75 Days}})
\end{aligned}$$

---

## 3. Side-by-Side Unit Economics Comparison Table

| Metric / Dimension | 🟢 Tier 1: Lite | 🔵 Tier 2: Tactical | 🟣 Tier 3: Solar Pro |
| :--- | :---: | :---: | :---: |
| **Production Hardware BOM** | **$59.50 (KES 7,735)** | **$135.00 (KES 17,550)** | **$235.00 (KES 30,550)** |
| **Setup / Installation Fee** | $27.00 (KES 3,500) | $58.00 (KES 7,500) | $115.00 (KES 15,000) |
| **Monthly Subscription (MRR)** | **$49.00 (KES 6,500)** | **$73.00 (KES 9,500)** | **$104.00 (KES 13,500)** |
| **Monthly Cloud & IoT OpEx** | $5.38 (KES 700) | $7.30 (KES 950) | $10.77 (KES 1,400) |
| **Monthly Net Cash Profit** | **$44.62 (KES 5,800)** | **$65.70 (KES 8,550)** | **$93.08 (KES 12,100)** |
| **Gross Contribution Margin** | **89.2%** | **90.0%** | **89.6%** |
| **Net Payback Period (Days)** | **39 Days** ⚡ | **43–61 Days** | **38–75 Days** |
| **3-Year Customer LTV** | **$1,606.32 USD** | **$2,365.20 USD** | **$3,350.88 USD** |
| **Blended CAC** | $35.00 USD | $50.00 USD | $85.00 USD |
| **LTV / CAC Ratio** | **45.9x** | **47.3x** | **39.4x** |
