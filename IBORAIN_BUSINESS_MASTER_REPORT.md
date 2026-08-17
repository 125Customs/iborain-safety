# 📊 Iborain Safety — Master Commercial & Financial Execution Report
*Private Commercial Blueprint & Investor / Partnership Dossier*

**Company:** Iborain Safety Ltd. (Nairobi, Kenya)  
**Hardware Incubation Partner:** [ChipuRobo STEM Makerspaces](https://chipurobo.com/)  
**Core Model:** Hardware-Enabled B2B SaaS & Installer Micro-Franchise Network  
**Target Market:** Sub-Saharan Africa (Beachhead: Nairobi Metro, Kenya)  
**Currency Standard:** Kenyan Shillings (KES) & US Dollars (USD @ 1 USD = 130 KES)

---

## 1. Executive Summary & Value Proposition

**Iborain Safety** solves the **$4 Billion Public Safety Blindspot** in emerging markets. In Sub-Saharan Africa, over 70% of violent and property crimes (carjackings, home burglaries, cargo diversion, armed robbery) are transit-borne, executed using getaway vehicles with cloned/muddy plates and unregistered motorcycles (*Boda Bodas*).

Existing Western solutions (such as Flock Safety at $5,000/camera/year) price out 99% of African communities and fail completely on local transit realities. Chinese CCTV cameras (Hikvision/Dahua) are dumb recording glass that only document crimes after they happen.

Iborain Safety delivers **Active, Real-Time Crime Elimination for $49/month (KES 6,500/mo) with Zero Upfront CapEx**:
1. **$110 Hardware BOM:** Built on Raspberry Pi Zero 2 W + Sony IMX500 AI Camera fabricated locally at ChipuRobo makerspaces.
2. **Sub-600ms AI Decision Engine:** Powered by Google Gemini (Gemini 3.7 Flash & Live API) on Google Cloud Run.
3. **M-Pesa Automated Billing:** Billed on the 1st of every month via automated Daraja API STK Push.
4. **Youth Franchise Flywheel:** Creating high-paying jobs where ChipuRobo-trained youth earn **KES 58,000/mo ($450/mo)** managing local sentry micro-franchises.

---

## 2. The 3 Ideal Customer Profiles (ICPs)

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 THE 3 CORE REVENUE SEGMENTS                                      │
├────────────────────────────────┬────────────────────────────────┬────────────────────────────────┤
│ 🏡 ICP 1: Gated Communities    │ 🚛 ICP 2: Logistics & SACCOs   │ 🏙️ ICP 3: Municipal Corridors  │
│    & Residential Estates       │    Commercial Hubs             │    & Business Districts (BIDs) │
├────────────────────────────────┼────────────────────────────────┼────────────────────────────────┤
│ • Decision Maker: Estate       │ • Decision Maker: Logistics    │ • Decision Maker: Ward Reps,   │
│   Chairman / Security Comm.    │   Director / SACCO Chairman    │   Business Associations        │
│ • Pain: Boda burglaries,       │ • Pain: Cargo theft, fuel      │ • Pain: Highway crime, getaway  │
│   unauthorized entries, slow   │   siphoning, unverified night  │   escape routes, unmonitored   │
│   paper logbooks.              │   fleet movements.             │   commercial streets.          │
│ • Package: Package A ($49/mo)  │ • Package: Package B ($72/mo)  │ • Package: Package C ($90/mo)  │
└────────────────────────────────┴────────────────────────────────┴────────────────────────────────┘
```

---

## 3. Product Packages & Pricing Architecture

### Package A: The Community Zero-CapEx Safety Lease (High Volume)
* **Target:** Residential gated courts, apartment clusters, school perimeters.
* **Upfront Hardware Cost:** **KES 0 ($0 CapEx)**
* **One-Time Network Setup & Calibration:** **KES 3,500 ($27 USD)**
* **Monthly SaaS Subscription:** **KES 6,500 / month ($49 USD)** per sentry node.
* **Contract Term:** 12-month auto-renewing contract.
* **Includes:** 24/7 Gemini transit fingerprinting, community WhatsApp security alerts, digital visitor logs, active GC9A01 / LED deterrence strobe, FreeForm™ crime investigation search.

### Package B: Commercial Logistics & SACCO Sentry
* **Target:** Transport SACCO stages, petrol stations, warehouse yards, factory gates.
* **Upfront Hardware Cost:** **KES 5,000 ($38 USD)**
* **Monthly SaaS Subscription:** **KES 9,500 / month ($72 USD)** per sentry node.
* **Includes:** High-speed fleet logging, cargo profiling (gas cylinders, courier bags, freight), plate mud-delta OCR, priority law enforcement dispatch export.

### Package C: Municipal Off-Grid Solar Corridor Node (Tier 2 Pro)
* **Target:** Street light poles, arterial road junctions, highway feeder points.
* **One-Time Pole Installation & Solar Mounting:** **KES 15,000 ($115 USD)**
* **Monthly SaaS Subscription:** **KES 12,000 / month ($90 USD)** per node.
* **Includes:** 100% off-grid 30W solar + LiFePO4 battery, dual-SIM 4G LTE IoT failover, 30-meter high-power night vision IR array, regional crime hotlist inter-community mesh.

---

## 4. Hardware Unit Economics & BOM Breakdown

### Tier 1 Live Demo & Checkpoint Node (Fabricated at ChipuRobo)

| Component | Sourcing Channel | Unit Cost (USD) | Unit Cost (KES) | % of BOM |
| :--- | :--- | :---: | :---: | :---: |
| **Raspberry Pi Zero 2 W** | Official RPi Distro / ChipuRobo | $25.00 | KES 3,250 | 22.7% |
| **Raspberry Pi AI Camera (Sony IMX500)** | ChipuRobo Lab Stock | $70.00 | KES 9,100 | 63.6% |
| **MAX98357A I2S DAC Amp + 3W Speaker** | Electronics Wholesale | $6.00 | KES 780 | 5.5% |
| **MPU-6500 6-Axis Anti-Tamper IMU** | Lab Stock | $2.00 | KES 260 | 1.8% |
| **TCRT5000 IR Optical Tripwire** | Sensor Importer | $1.00 | KES 130 | 0.9% |
| **3D Printed UV Enclosure & Mount** | ChipuRobo 3D Print Farm | $4.00 | KES 520 | 3.6% |
| **Misc (Wiring Harness, Glands, Screws)**| Local Hardware | $2.00 | KES 260 | 1.8% |
| **TOTAL TIER 1 PRODUCTION BOM** | **Complete Battle-Ready Sentry** | **$110.00** | **KES 14,200** | **100.0%** |

---

## 5. Monthly Cash Flow & Unit Economics (Per Node)

$$\begin{aligned}
\text{Monthly Recurring Revenue (MRR)} &= \text{KES } 6,500 \text{ (\$49.00 USD)} \\
\text{Less: Google Cloud Run Compute} &= -\text{KES } 260 \text{ (-\$2.00 USD)} \\
\text{Less: Gemini 3.7 Flash API Tokens} &= -\text{KES } 195 \text{ (-\$1.50 USD)} \\
\text{Less: 4G LTE IoT SIM Data (Safaricom/Airtel)} &= -\text{KES } 245 \text{ (-\$1.88 USD)} \\
\hline
\mathbf{\text{Monthly Net Contribution Margin}} &= \mathbf{\text{KES } 5,800 \text{ (\$44.62 USD)}} \\
\mathbf{\text{Gross Contribution Margin \%}} &= \mathbf{89.2\%}
\end{aligned}$$

### Capital Payback Period:
$$\text{Payback Time} = \frac{\text{Production BOM (KES 14,200)}}{\text{Monthly Net Cash Flow (KES 5,800)}} = \mathbf{2.44 \text{ Months (74 Days)}}$$

### Lifetime Value (LTV) & Customer Acquisition Cost (CAC):
* **Average Customer Lifespan:** 36 Months (3 Years)
* **LTV (Gross Profit over 36 mo):** $36 \times \$44.62 = \mathbf{\$1,606.32 \text{ USD (KES 208,820)}}$
* **Blended CAC (Direct Estate Sales):** $\mathbf{\$35.00 \text{ USD (KES 4,550)}}$
* **LTV / CAC Ratio:** $\mathbf{45.9\times}$ *(Venture standard is $>3\times$; Iborain delivers exceptional unit efficiency)*

---

## 6. Growth Projections & Cash Flow Scaling

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 SCALING COHORTS & CASH FLOW MODEL                                │
├───────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────────────────┤
│ Milestone │ Active Nodes │ Monthly MRR  │ Annual ARR   │ Monthly Net  │ Annual Net Cash Profit   │
├───────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────────────────┤
│ Pilot     │ 10 Nodes     │ KES 65,000   │ KES 780,000  │ KES 58,000   │ KES 696,000 ($5,350)     │
│ Stage 1   │ 50 Nodes     │ KES 325,000  │ KES 3.90M    │ KES 290,000  │ KES 3.48M ($26,760)      │
│ Stage 2   │ 150 Nodes    │ KES 975,000  │ KES 11.70M   │ KES 870,000  │ KES 10.44M ($80,300)     │
│ Stage 3   │ 500 Nodes    │ KES 3.25M    │ KES 39.00M   │ KES 2.90M    │ KES 34.80M ($267,690)    │
│ Scale     │ 1,500 Nodes  │ KES 9.75M    │ KES 117.00M  │ KES 8.70M    │ KES 104.40M ($803,000)   │
└───────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────────────────┘
```

---

## 7. 5-Year Pro-Forma Income Statement (USD)

| Line Item | Year 1 (150 Units) | Year 2 (500 Units) | Year 3 (1,500 Units) | Year 4 (4,000 Units) | Year 5 (10,000 Units) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Gross Subscription Revenue** | $88,200 | $294,000 | $882,000 | $2,352,000 | $5,880,000 |
| **Setup & Installation Fees** | $4,050 | $13,500 | $40,500 | $108,000 | $270,000 |
| **Total Gross Revenue** | **$92,250** | **$307,500** | **$922,500** | **$2,460,000** | **$6,150,000** |
| Hardware Production (COGS) | ($16,500) | ($55,000) | ($165,000) | ($440,000) | ($1,100,000) |
| Cloud Run & Gemini API Costs | ($4,500) | ($15,000) | ($45,000) | ($120,000) | ($300,000) |
| 4G IoT Cellular SIM Data | ($3,380) | ($11,280) | ($33,840) | ($90,240) | ($225,600) |
| **Gross Profit** | **$67,870** | **$226,220** | **$678,660** | **$1,809,760** | **$4,524,400** |
| *Gross Margin %* | *73.6%* | *73.6%* | *73.6%* | *73.6%* | *73.6%* |
| Sales & Marketing (Installer Comm.) | ($8,500) | ($25,000) | ($70,000) | ($180,000) | ($420,000) |
| Engineering & ChipuRobo Support | ($12,000) | ($36,000) | ($85,000) | ($180,000) | ($350,000) |
| G&A, Legal, Data Protection Audit | ($4,000) | ($10,000) | ($25,000) | ($60,000) | ($120,000) |
| **EBITDA / Operating Profit** | **$43,370** | **$155,220** | **$498,660** | **$1,389,760** | **$3,634,400** |
| *EBITDA Margin %* | *47.0%* | *50.5%* | *54.1%* | *56.5%* | *59.1%* |

---

## 8. The ChipuRobo Youth Micro-Franchise Flywheel

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               THE INSTALLER NETWORK REVENUE SHARE                                │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. Upfront Assembly Bounty:     KES 1,000 ($8 USD) paid to youth per unit assembled at ChipuRobo.│
│ 2. Installation Bounty:         KES 2,000 ($15 USD) paid upon verified pole/gate mounting.       │
│ 3. Monthly Recurring Royalty:   KES 1,500 ($12 USD) / month per active node for field servicing. │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### What an Installer Earns Managing 10 Nodes:
$$\text{Monthly Maintenance Income} = 10 \text{ Nodes} \times \text{KES } 1,500 = \text{KES } 15,000 \text{/mo}$$
$$\text{New Node Installations (4 new/mo)} = 4 \times \text{KES } 3,000 = \text{KES } 12,000 \text{/mo}$$
$$\text{Total Youth Technician Monthly Income} = \mathbf{\text{KES } 27,000 \text{ to KES } 58,000 \text{/mo (\$210 - \$450 USD/mo)}}$$

* **Economic Reality:** In Kenya, minimum wage is ~KES 15,200/mo. An Iborain installer earns **2x to 3.8x minimum wage** while maintaining neighborhood public safety.

---

## 9. Sales Pitch Playbook & Objections Handling (For Estate Chairmen)

### Objection 1: *"We already have physical security guards (askaris)."*
* **The Rebuttal:**  
  > *"Askaris are great for opening gates, but they cannot remember 500 license plates or detect a cloned plate from a robbery in Ruiru 20 minutes ago. When guards sleep at 3 AM or write wrong numbers in the black book, your estate is blind. Iborain Safety doesn't replace your guards—it acts as your guards' superhuman AI copilot, sounding an instant alarm and pinging their WhatsApp before a suspect even reaches the barrier."*

### Objection 2: *"We already have CCTV cameras installed."*
* **The Rebuttal:**  
  > *"CCTV is passive glass. Nobody sits watching 24 hours of video. When a house gets broken into, you spend 3 days scrubbing blurry footage on a dusty DVR only to find the camera didn't catch the plate. Iborain is active AI: it reads the plate, identifies the Boda cargo, flags the hotlist, and stops the crime in real time."*

### Objection 3: *"We don't have budget for expensive technology right now."*
* **The Rebuttal:**  
  > *"That’s exactly why we created the Zero-CapEx Lease. You pay KES 0 for the hardware. It is only KES 6,500/month, which comes out to less than KES 150 per household per month—cheaper than a loaf of bread. We install it free for 14 days; if your residents don't love the instant WhatsApp clearance, we remove it at zero charge."*

### Objection 4: *"What about Kenya Power blackouts and internet cuts?"*
* **The Rebuttal:**  
  > *"Every Iborain unit has battery backup and dual-SIM Safaricom/Airtel 4G LTE IoT failover. If Kenya Power goes off, the sentry stays alive. If cellular drops, the local chip caches the hotlist and sounds the physical voice alarm locally."*

---

## 10. Automated Billing & Collections (M-Pesa Daraja API)

1. **Automated STK Push:** On the 1st of every month at 9:00 AM, our backend fires an M-Pesa STK Push directly to the Estate Treasurer's registered phone.
2. **Instant Receipt & WhatsApp Audit:** Upon PIN entry, Daraja Webhook confirms payment $\rightarrow$ sends an automated PDF receipt and monthly crime audit log to the Estate Security WhatsApp group.
3. **Grace Period & Remote Lock:** If unpaid by the 7th of the month, the backend sends a gentle WhatsApp reminder. On the 10th, the visual beacon switches to standby until resolved, ensuring near-zero payment defaults.
