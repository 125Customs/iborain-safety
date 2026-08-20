# 🚀 Iborain Safety — Master Launch, Fabrication & Sales Execution Checklist
*The Ductile Production Architecture: Streamlined, Stealth, Solar-Ready Public Safety Sentry*

**Company:** Iborain Safety Ltd. (Nairobi, Kenya)  
**Fabrication Hub:** [ChipuRobo STEM Makerspaces](https://chipurobo.com/)  
**Core Architecture:** Ultra-Lean Edge Vision (Raspberry Pi Zero 2 W + Sony/Pi Camera + MPU-6500 Anti-Tamper + Dual Status LED)

---

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 THE 6-PHASE MASTER LAUNCH ROADMAP                                │
├────────────────────────────────┬─────────────────────────────────────────────────────────────────┤
│ 🟢 Phase 1: Bench Demo Rig     │ Solder 3-chip perfboard, connect camera & IMU, verify loop.     │
├────────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ 🔵 Phase 2: 3D Print Packaging │ Single-aperture weatherproof PETG box + universal pole clamp.   │
├────────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ 🟣 Phase 3: Cloud & Web Infra  │ Deploy Cloud Run broker, live landing page, M-Pesa & WhatsApp.  │
├────────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ 🟡 Phase 4: Field Calibration  │ Optical telephoto focus (3-10m), 4G LTE cellular soak test.     │
├────────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ 🔴 Phase 5: 14-Day Pilot Sales │ Estate Chairman pitch, gate mounting, 14-day M-Pesa conversion. │
├────────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ 🟠 Phase 6: Youth Franchise    │ Train ChipuRobo installers, 10-node franchises (KES 58k/mo).    │
└────────────────────────────────┴─────────────────────────────────────────────────────────────────┘
```

---

## 🟢 PHASE 1: The Bench Demo & Live Scanning Rig (Do This First)

*Objective: Assemble your streamlined 3-chip physical electronics on a clean perfboard and verify live multimodal scanning with Google Gemini.*

### 1.1 Physical Hardware Soldering & Wiring (Zero Clutter)
- [ ] **Mount Raspberry Pi Zero 2 W:** Solder male 40-pin GPIO header pins.
- [ ] **Connect Vision Sensor:** Attach the Camera Module (Sony IMX500 / 12MP Camera) ribbon cable to the CSI camera port (blue stiffener tab facing the board).
- [ ] **Wire Anti-Tamper & Anti-Theft Sensor (MPU-6500 6-Axis IMU):**
  - [ ] Connect `SDA` to Raspberry Pi `GPIO 2` (Pin 3).
  - [ ] Connect `SCL` to Raspberry Pi `GPIO 3` (Pin 5).
  - [ ] Connect `VCC` to `3.3V Rail` (Pin 1).
  - [ ] Connect `GND` to `Common Ground` (Pin 9).
- [ ] **Wire Status / Strobe LED ($0.50):**
  - [ ] Connect Anode (+) to `GPIO 24` (Pin 18) through a 220Ω resistor.
  - [ ] Connect Cathode (-) to `Common Ground` (Pin 20).
- [ ] **Wire Optical Arrival Tripwire (TCRT5000 IR Sensor):**
  - [ ] Connect `DO (Digital Out)` to `GPIO 17` (Pin 11).
  - [ ] Connect `VCC` to `3.3V` (Pin 17) and `GND` to Common Ground (Pin 25).

```
                              ┌─────────────────────────┐
                              │  Raspberry Pi Zero 2 W  │
                 3.3V Power ──┤ [1]  (3V3)    (5V)  [2] ├── 5V Power In (from Buck/Adapter)
     (I2C SDA -> MPU-6500) ───┤ [3]  (GPIO2)  (5V)  [4] │
     (I2C SCL -> MPU-6500) ───┤ [5]  (GPIO3)  (GND) [6] ├── Common Ground
                              │ [7]  (GPIO4)  (TXD) [8] │
                 Common GND ──┤ [9]  (GND)    (RXD) [10]│
 (TCRT5000 IR Tripwire DO) ───┤ [11] (GPIO17) (IO18)[12]│
                              │ [13] (GPIO27) (GND) [14]│
                              │ [15] (GPIO22) (IO23)[16]│
                 3.3V Power ──┤ [17] (3V3)    (IO24)[18]├── GPIO 24 (Status/Strobe LED +)
                              │ [19] (MOSI)   (GND) [20]├── Common GND (LED GND via 220Ω)
                              │ [21] (MISO)   (IO25)[22]│
                              │ [23] (SCLK)   (CE0) [24]│
                 Common GND ──┤ [25] (GND)    (CE1) [26]│
                              └─────────────────────────┘
```

### 1.2 Firmware & Software Verification
- [ ] **Flash OS:** Flash Raspberry Pi OS (64-bit Lite/Bookworm) onto a 32GB MicroSD card.
- [ ] **Install Dependencies:** `sudo apt-get update && sudo apt-get install -y python3-pip python3-opencv libcamera-tools i2c-tools`.
- [ ] **Run Hardware Smoke Test:**
  - [ ] Execute `python3 apps/pi-client/test_hardware.py`.
  - [ ] Verify I2C bus scan detects `0x68` (MPU-6500 IMU).
  - [ ] Verify Status LED pulses green (idle) and flashes red (threat trigger).
- [ ] **Live Gemini Vision Loop Verification:**
  - [ ] Start Cloud Run or local broker: `MODE=gemini pnpm run dev:backend`.
  - [ ] Launch edge client: `python3 apps/pi-client/robot.py --url ws://localhost:8080/ws/device`.
  - [ ] Hold up printed license plate `KDA 482B` or Boda Boda photo $\rightarrow$ verify Gemini returns transit fingerprint in sub-600ms and sends simulated WhatsApp alert.

---

## 🔵 PHASE 2: 3D Printing & Enclosure Packaging (At ChipuRobo)

*Objective: Fabricate a clean, sealed, single-aperture outdoor enclosure with universal pole mounting.*

### 2.1 3D CAD & Slicing Setup
- [ ] **Material:** **PETG or ASA** (UV and heat resistant; never use PLA for outdoor Nairobi sun).
- [ ] **Print Settings:** 0.20mm layer height, 4 outer walls, 25% Gyroid infill.
- [ ] **Print Component 1 (Main Casing Box):** Compact enclosure housing Pi Zero 2, IMU, and power stepdown.
- [ ] **Print Component 2 (Front Faceplate):** Single 20mm camera lens aperture + 5mm status LED hole. (Zero speaker grilles, zero LCD cutouts).
- [ ] **Print Component 3 (Sun/Rain Visor Hood):** 25mm overhang hood protecting lens from direct rain and sunlight glare.
- [ ] **Print Component 4 (Universal Pole Mount):** Curved rear bracket with dual 15mm slots for stainless jubilee hose clamps.

### 2.2 Assembly & Waterproof Sealing
- [ ] **Optical Window:** Install a 2mm circular anti-reflective acrylic/glass window over the camera aperture using neutral-cure silicone sealant.
- [ ] **LED Seal:** Insert 5mm rubber LED bezel grommet.
- [ ] **Cable Gland:** Thread power/solar cables through an **IP68 PG7 waterproof cable gland**.
- [ ] **Anti-Tamper Mount:** Fasten MPU-6500 IMU firmly to inner chassis wall using two M2 screws for direct vibration coupling.
- [ ] **Internal Fasteners:** Secure Pi Zero 2 onto threaded brass standoffs using M2.5 stainless steel screws.

---

## 🟣 PHASE 3: Production Cloud & Web Infrastructure Deployment

*Objective: Launch the public web presence, Google Cloud Run backend, WhatsApp dispatch webhook, and M-Pesa billing engine.*

### 3.1 Google Cloud Run Backend (`apps/backend`)
- [ ] Set environment secrets in Google Secret Manager (`GEMINI_API_KEY`, `DEVICE_AUTH_TOKENS`, `WHATSAPP_TOKEN`).
- [ ] Execute automated deployment: `GCP_PROJECT=your-project-id MODE=gemini bash apps/backend/deploy.sh`.
- [ ] Verify Cloud Run configuration: `--min-instances=1`, `--session-affinity=true`, `--timeout=3600s`.
- [ ] Verify live WebSocket URL: `wss://iborain-broker-<hash>.a.run.app/ws/device`.

### 3.2 Public Web Landing Page (`apps/landing`)
- [ ] Build Next.js application: `cd apps/landing && pnpm build`.
- [ ] Deploy to production hosting (Vercel / Cloud Run) on custom domain (`iborain.com` / `iborainsafety.com`).
- [ ] Verify sections: Hero, Streamlined Hardware Flip Cards (Tier 1-3), Interactive Terminal, and Pricing/Waitlist matrix.

### 3.3 WhatsApp Business & M-Pesa Daraja Integration
- [ ] **WhatsApp Cloud API:** Configure webhook to dispatch instant JSON alert payloads (Photo proof + Plate + Cargo) directly to registered security group chats in under 1 second.
- [ ] **M-Pesa Daraja API:** Configure automated STK Push recurring billing scheduled for the 1st of every month.

---

## 🟡 PHASE 4: Field Testing & Optical Calibration

*Objective: Calibrate camera focus and cellular reliability in realistic outdoor conditions.*

### 4.1 Optical & Scene Calibration
- [ ] **Focal Distance:** Adjust telephoto lens focus at **3 meters, 6 meters, and 10 meters** for maximum plate sharpness.
- [ ] **Night Vision:** Verify infrared LED array illuminates plates in pitch-black 0-lux conditions without blinding overexposure.
- [ ] **Angle Optimization:** Set mounting pitch to **15° downward tilt** to eliminate oncoming headlight glare.

### 4.2 Cellular & Network Resilience
- [ ] **SIM Card Activation:** Install Safaricom/Airtel IoT SIM card with active 4G data bundle.
- [ ] **24-Hour Soak Test:** Run continuous edge client connected to Cloud Run broker for 24 hours over 4G.
- [ ] **Fault Recovery:** Disconnect antenna $\rightarrow$ verify unit buffers logs locally in SQLite and auto-reconnects within 5 seconds of signal restoration.

---

## 🔴 PHASE 5: The 14-Day Pilot Customer Rollout (Selling to Estates)

*Objective: Deploy working sentry units to your 3 pilot estate security committees and convert them into paying monthly subscriptions.*

### 5.1 The Chairman Pitch & Agreement
- [ ] **Target:** Meet with Estate Security Committee Chairman & Treasurer (e.g. Syokimau Court, Ruiru Gated Court, Membley).
- [ ] **The Offer:** *"We install the complete Iborain Safety system at your gate today for KES 0 upfront. Test it for 14 days. If your residents don't love the instant WhatsApp clearance and security alerts, we take it down for free."*
- [ ] **Execute Pilot Agreement:** Sign the 14-Day Zero-CapEx Safety Lease Pilot Form.

### 5.2 On-Site Gate Installation (Takes 20 Minutes)
- [ ] **Mounting:** Strap enclosure securely to barrier post or light pole at **2.4 meters height** using stainless steel jubilee straps.
- [ ] **Power:** Plug 5V/3A power adapter into gatehouse AC outlet (or connect 30W solar panel).
- [ ] **Group Setup:** Create official estate security WhatsApp group (add Estate Chairman, Security Committee, and Head Guard).
- [ ] **Guard Onboarding (3 Minutes):** Show the security guards (*askaris*) how threat cards ping directly on their WhatsApp.

### 5.3 Day 1 to 14 Pilot Monitoring & Conversion
- [ ] **Day 3 Check-In:** Verify guards are receiving WhatsApp clearance cards smoothly.
- [ ] **Day 7 Mid-Pilot Report:** Send an automated 1-page PDF summary to the Estate Chairman showing total vehicles fingerprinted (e.g. *1,420 entries, 0 unauthorized breaches*).
- [ ] **Day 14 Final Conversion:**
  - [ ] Present monthly crime elimination report at committee meeting.
  - [ ] Sign 12-month recurring contract (**KES 6,500/month**).
  - [ ] Trigger initial M-Pesa STK Push to Estate Treasurer.

---

## 🟠 PHASE 6: Scaling the ChipuRobo Youth Installer Network

*Objective: Transform local youth technicians into independent micro-franchisees who assemble, install, and maintain sentry clusters.*

### 6.1 Assembly Line Training at ChipuRobo
- [ ] **Standardized Assembly SOP:** Standardize the **15-minute 3-chip assembly manual** (Pi Zero 2 + Camera + IMU + LED).
- [ ] **Quality Assurance (QA) Checklist:** Every assembled unit passes:
  1. 5-minute burn-in test on `test_hardware.py`.
  2. Submersion spray test (IP66 seal check).
  3. Camera focus test at 5 meters.
- [ ] **Technician Compensation:** Pay **KES 1,000 ($8 USD)** cash bounty to student technicians per verified unit assembled.

### 6.2 Franchise Expansion (10 Nodes per Installer)
- [ ] Assign certified installers to 10-node clusters; installers earn **KES 30,400 to KES 58,000/month ($233 - $450 USD/mo)** in recurring maintenance royalties.
