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

Existing Western ALPR systems (Flock Safety at $5,000/camera/year) are cost-prohibitive for 99% of African communities and fail completely on local transit realities (muddy plates, modified Proboxes, informal cargo). Dumb CCTV systems (Hikvision/Dahua) only record passive video without active deterrence or instant alerts.

Iborain delivers **Active, Real-Time Crime Elimination starting at $49/month (KES 6,500/mo) with Zero Upfront CapEx**, powered by Google Gemini (Gemini 3.7 Flash & Live API) on Google Cloud Run and modular edge sentry hardware fabricated locally at ChipuRobo makerspaces in Nairobi.

---

## 2. The 3 Hardware Tiers: Full Bill of Materials & Manufacturing Specs

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 THE 3 IBORAIN HARDWARE TIERS                                     │
├────────────────────────────────┬────────────────────────────────┬────────────────────────────────┤
│ 🟢 Tier 1: Iborain Lite        │ 🔵 Tier 2: Iborain Tactical    │ 🟣 Tier 3: Iborain Solar Pro   │
│    (High-Velocity Checkpoint)  │    (Neural Transit Sentry)     │    (Off-Grid Corridor Node)    │
├────────────────────────────────┼────────────────────────────────┼────────────────────────────────┤
│ • BOM Cost: $68 (KES 8,840)    │ • BOM Cost: $148 (KES 19,240)  │ • BOM Cost: $258 (KES 33,540)  │
│ • Subscription: $49/mo (6.5k)  │ • Subscription: $73/mo (9.5k)  │ • Subscription: $104/mo (13.5k)│
│ • Payback: 46 Days (1.5 mo)    │ • Payback: 68 Days (2.2 mo)    │ • Payback: 84 Days (2.8 mo)    │
│ • Power: AC/Grid (5V/2A)       │ • Power: AC / 12V Grid + 4G    │ • Power: 100% Solar + LiFePO4  │
└────────────────────────────────┴────────────────────────────────┴────────────────────────────────┘
```

---

### 🟢 TIER 1: Iborain Lite (The High-Velocity Checkpoint Node)

**Ideal Deployment:** Residential estate barrier gates, school entrances, quiet gated courts, church perimeters (Grid-powered, Wi-Fi or basic 4G).

#### 1. Material & Component Bill of Materials (BOM)

| Subsystem / Part | Technical Specification | Unit Cost (USD) | Unit Cost (KES) | Sourcing / Fabrication |
| :--- | :--- | :---: | :---: | :--- |
| **Compute Board** | Raspberry Pi Zero 2 W (Quad-Core 64-bit ARM) | $25.00 | KES 3,250 | Official RPi Distro / ChipuRobo |
| **Vision Sensor** | Raspberry Pi Camera Module 3 (12MP Sony IMX708 Autofocus/HDR) | $25.00 | KES 3,250 | Camera Supplier |
| **Acoustic Deterrence** | MAX98357A I2S 3W Class D DAC + 3W Weatherproof Speaker | $6.00 | KES 780 | Audio Component Wholesaler |
| **Anti-Tamper Sensor** | MPU-6500 6-Axis Gyro/Accelerometer (I2C 0x68) | $2.00 | KES 260 | ChipuRobo Lab Stock |
| **Optical Tripwire** | TCRT5000 Infrared Reflective Sensor (GPIO 17) | $1.00 | KES 130 | Sensor Importer |
| **3D Printed Enclosure** | 140g UV-Resistant PETG filament ($2.80) + 3D Print Machine Time ($1.20) | $4.00 | KES 520 | ChipuRobo 3D Print Farm |
| **Power Supply** | 5V 3A AC/DC Wall Adapter with Surge Protection | $3.00 | KES 390 | Electronics Wholesale |
| **Hardware & Fasteners** | Stainless M3 Screws, Weatherproof Cable Gland, JST Wire Harness | $2.00 | KES 260 | Local Hardware Sourcing |
| **TOTAL TIER 1 BOM** | **Complete Assembled Iborain Lite Node** | **$68.00** | **KES 8,840** | **100% Fully Built** |

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
\mathbf{\text{Capital Payback Period}} &= \frac{\text{KES } 8,840}{\text{KES } 5,800 \text{/mo}} = \mathbf{1.52 \text{ Months (46 Days)}}
\end{aligned}$$

---

### 🔵 TIER 2: Iborain Tactical (The Neural Transit & SACCO Sentry)

**Ideal Deployment:** Transport SACCO stages, warehouse logistics yards, commercial petrol stations, high-traffic gated communities (Grid-powered or 12V line, 4G LTE, live LCD radar).

#### 1. Material & Component Bill of Materials (BOM)

| Subsystem / Part | Technical Specification | Unit Cost (USD) | Unit Cost (KES) | Sourcing / Fabrication |
| :--- | :--- | :---: | :---: | :--- |
| **Compute Board** | Raspberry Pi Zero 2 W (Quad-Core 64-bit ARM) | $25.00 | KES 3,250 | Official RPi Distro / ChipuRobo |
| **Neural AI Camera** | Raspberry Pi AI Camera (12.3MP Sony IMX500 with On-Chip Neural DSP) | $70.00 | KES 9,100 | ChipuRobo Lab Stock |
| **Visual Sentry HUD** | GC9A01 1.28" Round IPS LCD (Threat Beacon & Radar Display) | $4.00 | KES 520 | Electronics Component Stock |
| **Cellular IoT Modem** | Quectel / Waveshare 4G LTE Cellular HAT + High-Gain Antenna | $24.00 | KES 3,120 | RF / Cellular Importer |
| **Acoustic Deterrence** | MAX98357A I2S 3W DAC Amp + 5W Weatherproof Horn Speaker | $7.00 | KES 910 | Audio Supplier |
| **Anti-Tamper Sensor** | MPU-6500 6-Axis Gyro/Accelerometer (I2C 0x68) | $2.00 | KES 260 | ChipuRobo Lab Stock |
| **Optical Tripwire** | TCRT5000 Infrared Reflective Sensor (GPIO 17) | $1.00 | KES 130 | Sensor Importer |
| **3D Printed Enclosure** | 220g PETG with Acrylic Lens Window ($4.40) + Machine Time ($1.60) | $6.00 | KES 780 | ChipuRobo 3D Print Farm |
| **Power Subsystem** | 12V to 5V 3A DC Buck Converter & Power Line Filter | $3.00 | KES 390 | Electronics Importer |
| **Pole Mounting Bracket**| Stainless Steel Adjustable Pole Clamp & Arm | $4.00 | KES 520 | Local Metal Fabrication |
| **Fasteners & Harness** | Stainless M3/M4 Screws, IP67 Cable Glands, JST Wire Harness | $2.00 | KES 260 | Local Hardware Sourcing |
| **TOTAL TIER 2 BOM** | **Complete Assembled Iborain Tactical Node** | **$148.00** | **KES 19,240** | **100% Fully Built** |

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
\mathbf{\text{Capital Payback Period}} &= \frac{\text{KES } 19,240 - \text{KES } 5,000 \text{ (Upfront)}}{\text{KES } 8,550 \text{/mo}} = \mathbf{1.66 \text{ Months (50 Days)}} \\
&(\text{Without Upfront: } \frac{\text{KES } 19,240}{\text{KES } 8,550} = \mathbf{2.25 \text{ Months / 68 Days}})
\end{aligned}$$

---

### 🟣 TIER 3: Iborain Solar Pro (The Off-Grid Corridor Node — "The Falcon Equivalent")

**Ideal Deployment:** Public street light poles, arterial highway feeder junctions, unpowered municipal avenues, remote commercial perimeters (100% Solar Off-Grid, Dual 4G + GPS, 30m Night Vision).

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
| **Acoustic Horn** | MAX98357A I2S 3W DAC Amp + 10W Heavy-Duty Weatherproof Horn | $9.00 | KES 1,170 | Industrial Audio Supplier |
| **Anti-Tamper Sensor** | MPU-6500 6-Axis Gyro/Accelerometer (I2C 0x68) | $2.00 | KES 260 | ChipuRobo Lab Stock |
| **Doppler Radar Sensor** | 10.525GHz Microwave Doppler Radar (15m wide-road detection) | $3.00 | KES 390 | Sensor Importer |
| **Industrial Enclosure** | IP66 Die-Cast Aluminum & Polycarbonate Box with Gore-Tex Vent | $16.00 | KES 2,080 | Industrial Plastics / Metal |
| **3D Printed Skeleton** | 280g PETG Internal Battery Sled, Shroud & Mounts ($5.60) | $5.00 | KES 650 | ChipuRobo 3D Print Farm |
| **Heavy-Duty Mount** | Galvanized Steel Universal Pole-Mount Arm & Stainless Straps | $8.00 | KES 1,040 | Local Metal Fabrication |
| **Glands, Screws & QA** | IP68 Waterproof Glands, Silicon O-Rings, Wire Harness, Assembly | $6.00 | KES 780 | ChipuRobo Makerspace QA |
| **TOTAL TIER 3 BOM** | **Complete Industrial Off-Grid Corridor Sentry** | **$258.00** | **KES 33,540** | **100% Fully Built** |

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
\mathbf{\text{Capital Payback Period}} &= \frac{\text{KES } 33,540 - \text{KES } 15,000 \text{ (Setup)}}{\text{KES } 12,100 \text{/mo}} = \mathbf{1.53 \text{ Months (46 Days)}} \\
&(\text{Without Setup: } \frac{\text{KES } 33,540}{\text{KES } 12,100} = \mathbf{2.77 \text{ Months / 84 Days}})
\end{aligned}$$

---

## 3. Side-by-Side Unit Economics Comparison Table

| Metric / Dimension | 🟢 Tier 1: Lite | 🔵 Tier 2: Tactical | 🟣 Tier 3: Solar Pro |
| :--- | :---: | :---: | :---: |
| **Production Hardware BOM** | **$68.00 (KES 8,840)** | **$148.00 (KES 19,240)** | **$258.00 (KES 33,540)** |
| **Setup / Installation Fee** | $27.00 (KES 3,500) | $58.00 (KES 7,500) | $115.00 (KES 15,000) |
| **Monthly Subscription (MRR)** | **$49.00 (KES 6,500)** | **$73.00 (KES 9,500)** | **$104.00 (KES 13,500)** |
| **Monthly Cloud & IoT OpEx** | $5.38 (KES 700) | $7.30 (KES 950) | $10.77 (KES 1,400) |
| **Monthly Net Cash Profit** | **$44.62 (KES 5,800)** | **$65.70 (KES 8,550)** | **$93.08 (KES 12,100)** |
| **Gross Contribution Margin** | **89.2%** | **90.0%** | **89.6%** |
| **Net Payback Period (Days)** | **46 Days** | **50–68 Days** | **46–84 Days** |
| **3-Year Customer LTV** | **$1,606.32 USD** | **$2,365.20 USD** | **$3,350.88 USD** |
| **Blended CAC** | $35.00 USD | $50.00 USD | $85.00 USD |
| **LTV / CAC Ratio** | **45.9x** | **47.3x** | **39.4x** |

---

## 4. Blended Portfolio Scaling Projections (150 to 5,000 Nodes)

*Assumes a realistic real-world deployment mix: 60% Tier 1 (Estates), 25% Tier 2 (SACCOs/Logistics), 15% Tier 3 (Off-Grid Municipal Corridors).*

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                  BLENDED PORTFOLIO CASH FLOW MODEL                               │
├───────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────────────────┤
│ Milestone │ Total Nodes  │ Monthly MRR  │ Annual ARR   │ Monthly Net  │ Annual Net Cash Profit   │
├───────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────────────────┤
│ Pilot     │ 10 Nodes     │ KES 73,000   │ KES 876,000  │ KES 65,400   │ KES 784,800 ($6,030)     │
│ Stage 1   │ 50 Nodes     │ KES 365,000  │ KES 4.38M    │ KES 327,000  │ KES 3.92M ($30,150)      │
│ Stage 2   │ 150 Nodes    │ KES 1.095M   │ KES 13.14M   │ KES 981,000  │ KES 11.77M ($90,550)     │
│ Stage 3   │ 500 Nodes    │ KES 3.65M    │ KES 43.80M   │ KES 3.27M    │ KES 39.24M ($301,840)    │
│ Scale     │ 1,500 Nodes  │ KES 10.95M   │ KES 131.40M  │ KES 9.81M    │ KES 117.72M ($905,530)   │
│ Pan-Africa│ 5,000 Nodes  │ KES 36.50M   │ KES 438.00M  │ KES 32.70M   │ KES 392.40M ($3.01M)     │
└───────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────────────────┘
```

---

## 5. The ChipuRobo Youth Franchise Revenue-Share Breakdown

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               INSTALLER BOUNTIES & ROYALTIES BY TIER                             │
├────────────────────────┬──────────────────────┬──────────────────────┬───────────────────────────┤
│ Tier                   │ Assembly Bounty (Lab)│ Installation Bounty  │ Monthly Servicing Royalty │
├────────────────────────┼──────────────────────┼──────────────────────┼───────────────────────────┤
│ 🟢 Tier 1: Lite        │ KES 800 ($6.15 USD)  │ KES 1,500 ($11.50)   │ KES 1,200/mo ($9.23 USD)  │
│ 🔵 Tier 2: Tactical    │ KES 1,200 ($9.23 USD)│ KES 2,500 ($19.23)   │ KES 1,800/mo ($13.85 USD) │
│ 🟣 Tier 3: Solar Pro   │ KES 2,000 ($15.38 USD│ KES 5,000 ($38.46)   │ KES 2,500/mo ($19.23 USD) │
└────────────────────────┴──────────────────────┴──────────────────────┴───────────────────────────┘
```

### What an Installer Earns Managing 10 Mixed Nodes:
$$\begin{aligned}
\text{Monthly Servicing Income (6 Tier 1 + 3 Tier 2 + 1 Tier 3)} &= (6 \times \text{KES } 1,200) + (3 \times \text{KES } 1,800) + (1 \times \text{KES } 2,500) \\
&= \text{KES } 7,200 + \text{KES } 5,400 + \text{KES } 2,500 = \mathbf{\text{KES } 15,100 \text{/mo}} \\
\text{New Monthly Installs (2 Tier 1 + 1 Tier 2 + 1 Tier 3)} &= (2 \times \text{KES } 2,300) + (1 \times \text{KES } 3,700) + (1 \times \text{KES } 7,000) \\
&= \text{KES } 4,600 + \text{KES } 3,700 + \text{KES } 7,000 = \mathbf{\text{KES } 15,300 \text{/mo}} \\
\hline
\mathbf{\text{Total Monthly Youth Income}} &= \mathbf{\text{KES } 30,400 \text{ to KES } 58,000 \text{/mo (\$233 - \$450 USD/mo)}}
\end{aligned}$$

---

## 6. Objection Handling Playbook for Sales Reps

### 1. "We already have physical security guards (*askaris*)."
> *"Askaris are great for opening gates, but they cannot remember 500 license plates or detect a cloned plate from a robbery in Ruiru 20 minutes ago. When guards sleep at 3 AM or write wrong numbers in the black book, your estate is blind. Iborain Safety doesn't replace your guards—it acts as your guards' superhuman AI copilot, sounding an instant alarm and pinging their WhatsApp before a suspect even reaches the barrier."*

### 2. "We already have CCTV cameras installed."
> *"CCTV is passive glass. Nobody sits watching 24 hours of video. When a house gets broken into, you spend 3 days scrubbing blurry footage on a dusty DVR only to find the camera didn't catch the plate. Iborain is active AI: it reads the plate, identifies the Boda cargo, flags the hotlist, and stops the crime in real time."*

### 3. "We don't have budget for expensive technology right now."
> *"That’s exactly why we created the Zero-CapEx Lease. You pay KES 0 for the hardware. It is only KES 6,500/month, which comes out to less than KES 150 per household per month—cheaper than a loaf of bread. We install it free for 14 days; if your residents don't love the instant WhatsApp clearance, we remove it at zero charge."*

### 4. "What about Kenya Power blackouts and internet cuts?"
> *"Every Iborain unit has battery backup and dual-SIM Safaricom/Airtel 4G LTE IoT failover. If Kenya Power goes off, the sentry stays alive. If cellular drops, the local chip caches the hotlist and sounds the physical voice alarm locally."*
