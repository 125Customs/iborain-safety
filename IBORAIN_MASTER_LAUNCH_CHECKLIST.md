# 🚀 Iborain Safety — Master Launch, Fabrication & Sales Execution Checklist
*The Complete End-to-End Operational Playbook: From Breadboard Demo to Live Market Rollout*

**Company:** Iborain Safety Ltd. (Nairobi, Kenya)  
**Fabrication Hub:** [ChipuRobo STEM Makerspaces](https://chipurobo.com/)  
**Document Purpose:** The single, definitive, step-by-step master checklist for building, packaging, deploying, and commercially selling Iborain Safety sentry nodes in Kenya.

---

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 THE 6-PHASE MASTER LAUNCH ROADMAP                                │
├────────────────────────────────┬─────────────────────────────────────────────────────────────────┤
│ 🟢 Phase 1: Bench Demo Rig     │ Solder perfboard, wire camera/speaker/sensors, verify code.     │
├────────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ 🔵 Phase 2: 3D Print Packaging │ Slice PETG/ASA enclosure, waterproof sealing, optical window.   │
├────────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ 🟣 Phase 3: Cloud & Web Infra  │ Deploy Cloud Run broker, live landing page, M-Pesa & WhatsApp.  │
├────────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ 🟡 Phase 4: Field Calibration  │ Optical focus, 4G cellular soak test, 85dB audio tuning.        │
├────────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ 🔴 Phase 5: 14-Day Pilot Sales │ Estate Chairman pitch, gate mounting, 14-day M-Pesa conversion. │
├────────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ 🟠 Phase 6: Youth Franchise    │ Train ChipuRobo installers, 10-node franchises (KES 58k/mo).    │
└────────────────────────────────┴─────────────────────────────────────────────────────────────────┘
```

---

## 🟢 PHASE 1: The Bench Demo & Live Scanning Rig (Do This First)

*Objective: Assemble your working physical electronics on a soldered perfboard/breadboard and verify 100% live multimodal scanning with Google Gemini.*

### 1.1 Physical Hardware Soldering & Wiring
- [ ] **Mount Raspberry Pi Zero 2 W:** Solder 40-pin GPIO male header pins securely.
- [ ] **Connect Vision Sensor:** Attach the Raspberry Pi AI Camera (Sony IMX500) ribbon cable to the CSI camera port (ensure the blue stiffener tab faces the board).
- [ ] **Wire Audio Deterrence Subsystem (MAX98357A I2S DAC Amp):**
  - [ ] Connect `LRC / FS` to Raspberry Pi `GPIO 19` (Pin 35).
  - [ ] Connect `BCLK / SCLK` to Raspberry Pi `GPIO 18` (Pin 12).
  - [ ] Connect `DIN` to Raspberry Pi `GPIO 21` (Pin 40).
  - [ ] Connect `VIN` to `5V Rail` (Pin 2).
  - [ ] Connect `GND` to `Common Ground` (Pin 6).
  - [ ] Solder 3W/5W 8-Ohm speaker wires to the `+` and `-` screw terminal output.
- [ ] **Wire Anti-Tamper & Anti-Vandalism Subsystem (MPU-6500 6-Axis IMU):**
  - [ ] Connect `SDA` to Raspberry Pi `GPIO 2` (I2C SDA - Pin 3).
  - [ ] Connect `SCL` to Raspberry Pi `GPIO 3` (I2C SCL - Pin 5).
  - [ ] Connect `VCC` to `3.3V Rail` (Pin 1).
  - [ ] Connect `GND` to `Common Ground` (Pin 9).
- [ ] **Wire Sentry Beacon HUD (GC9A01 1.28" Round LCD - Optional for Demo):**
  - [ ] Connect `DIN / MOSI` to `GPIO 10` (Pin 19).
  - [ ] Connect `SCLK` to `GPIO 11` (Pin 23).
  - [ ] Connect `CS` to `GPIO 8` (Pin 24).
  - [ ] Connect `DC` to `GPIO 24` (Pin 18).
  - [ ] Connect `RST` to `GPIO 25` (Pin 22).
  - [ ] Connect `VCC` to `3.3V` (Pin 17) and `GND` to Pin 20.
- [ ] **Wire Optical Arrival Tripwire (TCRT5000 IR Sensor):**
  - [ ] Connect `DO (Digital Out)` to `GPIO 17` (Pin 11).
  - [ ] Connect `VCC` to `3.3V` and `GND` to Common Ground.

### 1.2 Firmware & Software Verification
- [ ] **Flash OS:** Flash Raspberry Pi OS (64-bit Lite/Bookworm) onto a 32GB Class 10 MicroSD card.
- [ ] **Install Dependencies:** Run `sudo apt-get update && sudo apt-get install -y python3-pip python3-opencv libcamera-tools i2c-tools`.
- [ ] **Run Hardware Smoke Test:**
  - [ ] Execute `python3 apps/pi-client/test_hardware.py`.
  - [ ] Verify I2C bus scan detects `0x68` (MPU-6500 IMU).
  - [ ] Verify test audio chime plays crisply through the MAX98357A speaker.
  - [ ] Verify LCD displays the "IBORAIN SENTRY" circular radar graphic.
- [ ] **Live Gemini Vision Loop Verification:**
  - [ ] Start Cloud Run or local broker: `MODE=gemini pnpm run dev:backend`.
  - [ ] Launch edge client: `python3 apps/pi-client/robot.py --url ws://localhost:8080/ws/device`.
  - [ ] Hold up printed license plate `KDA 482B` and a Boda Boda photo $\rightarrow$ verify Gemini returns `set_sentry_state` in sub-600ms, triggering the speaker warning and simulated WhatsApp dispatch.

---

## 🔵 PHASE 2: 3D Printing & Enclosure Packaging (At ChipuRobo)

*Objective: Fabricate an industrial, weatherproof, sun-shielded enclosure to transform bench electronics into a rugged outdoor product.*

### 2.1 3D CAD & Slicing Setup
- [ ] **Select Filament Material:** Use **PETG or ASA** (Do NOT use basic PLA; PLA deforms and melts in the Nairobi afternoon sun).
- [ ] **Print Settings:** 0.20mm layer height, 4 outer perimeters/walls, 25% Gyroid infill for high impact resistance.
- [ ] **Print Component 1 (Main Casing Box):** Houses the Pi Zero 2, audio amp, IMU, and power converter.
- [ ] **Print Component 2 (Front Faceplate):** Features the camera lens aperture, speaker acoustic grille, and IR window.
- [ ] **Print Component 3 (Sun/Rain Visor Hood):** 25mm overhang hood that shields the camera lens from direct rain and lens flare.
- [ ] **Print Component 4 (Universal Pole Mount):** Curved rear bracket with dual 15mm slots for stainless steel jubilee hose clamps.

### 2.2 Assembly & Waterproof Sealing
- [ ] **Optical Window:** Install a 2mm anti-reflective acrylic/glass circular window over the camera aperture using neutral-cure silicone sealant.
- [ ] **Acoustic Gasket:** Install waterproof acoustic membrane (e.g. Gore acoustic vent) over the speaker grille to let sound out while blocking water.
- [ ] **Cable Gland:** Thread power/solar cables through an **IP68 PG7/PG9 waterproof cable gland**.
- [ ] **Anti-Tamper Mount:** Fasten the MPU-6500 IMU firmly to the inner chassis wall using two M2 screws (ensures direct vibration transfer).
- [ ] **Internal Fasteners:** Secure all circuit boards onto threaded brass heat-set inserts using M2.5 stainless steel screws.

---

## 🟣 PHASE 3: Production Cloud & Web Infrastructure Deployment

*Objective: Launch the public web presence, Google Cloud Run backend, WhatsApp dispatch webhook, and M-Pesa billing engine.*

### 3.1 Google Cloud Run Backend (`apps/backend`)
- [ ] Set environment variables in Google Secret Manager (`GEMINI_API_KEY`, `DEVICE_AUTH_TOKENS`, `WHATSAPP_TOKEN`).
- [ ] Execute automated deployment: `GCP_PROJECT=your-project-id MODE=gemini bash apps/backend/deploy.sh`.
- [ ] Verify Cloud Run configuration: `--min-instances=1`, `--session-affinity=true`, `--timeout=3600s`, `--memory=512Mi`.
- [ ] Verify live WebSocket URL: `wss://iborain-broker-<hash>.a.run.app/ws/device`.

### 3.2 Public Web Landing Page (`apps/landing`)
- [ ] Build and verify Next.js application: `cd apps/landing && pnpm build`.
- [ ] Deploy to production hosting (Vercel / Cloud Run) on custom domain (`iborain.com` / `iborainsafety.com`).
- [ ] Verify core sections:
  - [ ] **Hero Section:** Value proposition & 14-Day Risk-Free Trial CTA.
  - [ ] **Hardware Flip Cards:** Interactive 3D breakdown of Tier 1 ($68), Tier 2 ($148), and Tier 3 ($258).
  - [ ] **Interactive Terminal:** Live simulated transit forensics and tool-calling telemetry.
  - [ ] **Waitlist & Pricing Matrix:** KES 6,500/mo Package A with direct WhatsApp contact button.
  - [ ] **ChipuRobo Partnership Badge:** Verification of local manufacturing in Nairobi.

### 3.3 WhatsApp Business & M-Pesa Daraja Integration
- [ ] **WhatsApp Cloud API:** Configure webhook to dispatch instant JSON alert payloads (Photo proof + Plate + Cargo) to registered security group chats.
- [ ] **M-Pesa Daraja API:**
  - [ ] Register Daraja B2B Paybill / Till Number.
  - [ ] Configure automated STK Push recurring billing scheduled for the 1st of every month.
  - [ ] Configure IPN (Instant Payment Notification) webhook to generate automated digital PDF receipts.

---

## 🟡 PHASE 4: Field Testing & Optical Calibration

*Objective: Calibrate camera focus, cellular reliability, and audio volume in realistic outdoor conditions before customer delivery.*

### 4.1 Optical & Scene Calibration
- [ ] **Focal Distance:** Adjust lens focus at **3 meters, 6 meters, and 10 meters** for maximum plate sharpness.
- [ ] **Low-Light / Night Testing:** Verify infrared LED array illuminates plates in pitch-black 0-lux conditions without blinding overexposure (anti-reflective tuning).
- [ ] **Angle Optimization:** Set mounting pitch to **15° downward tilt** (minimizes headlight glare from oncoming vehicles).

### 4.2 Cellular & Network Resilience
- [ ] **SIM Card Activation:** Install Safaricom IoT SIM card with active 4G data bundle.
- [ ] **24-Hour Soak Test:** Run continuous edge client connected to Cloud Run broker for 24 hours over 4G.
- [ ] **Fault Injection:** Manually cut cellular connection $\rightarrow$ verify unit buffers logs locally in SQLite and auto-reconnects within 5 seconds of signal restoration.

### 4.3 Audio & Deterrence Calibration
- [ ] **Volume Tuning:** Calibrate MAX98357A output to **85 dB at 3 meters** (loud enough to be heard over idling diesel matatus without clipping).
- [ ] **IMU Shock Threshold:** Calibrate MPU-6500 to trigger a high-priority tamper alert if subjected to $>1.5G$ acceleration or $>10^\circ$ continuous tilt.

---

## 🔴 PHASE 5: The 14-Day Pilot Customer Rollout (Selling to Estates)

*Objective: Deploy working sentry units to your 3 pilot estate security committees and convert them into paying monthly subscriptions.*

### 5.1 The Chairman Pitch & Agreement
- [ ] **Target:** Meet with Estate Security Committee Chairman & Treasurer (e.g. Syokimau Court, Ruiru Gated Court, Membley).
- [ ] **The Offer:** *"We install the complete Iborain Safety system at your gate today for KES 0 upfront. Test it for 14 days. If your residents don't love the instant WhatsApp clearance and security alerts, we take it down for free."*
- [ ] **Execute Pilot Agreement:** Sign the 14-Day Zero-CapEx Safety Lease Pilot Form.

### 5.2 On-Site Gate Installation (Takes 30 Minutes)
- [ ] **Mounting:** Strap enclosure securely to the barrier post or street light pole at **2.4 meters height** using stainless steel jubilee straps.
- [ ] **Power:** Plug 5V/3A power adapter into the gatehouse AC outlet (or connect 30W solar panel).
- [ ] **Group Setup:** Create the official estate security WhatsApp group (add Estate Chairman, Security Committee, and Head Guard).
- [ ] **Guard Onboarding (5 Minutes):** Show the security guards (*askaris*) how the unit automatically chimes and sends the alert to their phone.

### 5.3 Day 1 to 14 Pilot Monitoring & Conversion
- [ ] **Day 3 Check-In:** Visit the gatehouse to verify guards are comfortable and review transit logs.
- [ ] **Day 7 Mid-Pilot Report:** Send an automated 1-page PDF summary to the Estate Chairman showing total vehicles fingerprinted (e.g. *1,420 entries, 0 unauthorized breaches*).
- [ ] **Day 14 Final Conversion:**
  - [ ] Present the monthly crime elimination report at the committee meeting.
  - [ ] Sign the 12-month recurring contract (**KES 6,500/month**).
  - [ ] Send the initial M-Pesa STK Push to the Estate Treasurer to establish automated billing.

---

## 🟠 PHASE 6: Scaling the ChipuRobo Youth Installer Network

*Objective: Transform local youth technicians into independent micro-franchisees who assemble, install, and maintain sentry clusters.*

### 6.1 Assembly Line Training at ChipuRobo
- [ ] **Standardized Assembly SOP:** Create a 20-minute visual assembly manual for ChipuRobo makerspace students.
- [ ] **Quality Assurance (QA) Checklist:** Every assembled unit must pass:
  1. 5-minute burn-in test on `test_hardware.py`.
  2. Submersion spray test (IP66 seal check).
  3. Camera focus test at 5 meters.
- [ ] **Technician Compensation:** Pay **KES 1,000 ($8 USD)** cash bounty to student technicians per verified unit assembled.

### 6.2 Franchise Expansion (10 Nodes per Installer)
- [ ] Assign certified installers to specific geographic zones (e.g. Syokimau Corridor, Ruiru Corridor, Westlands).
- [ ] Installers receive **KES 2,000** for each new estate installation + **KES 1,500/month** recurring maintenance royalty per active node.
- [ ] **Installer Income:** Managing 10 sentry nodes earns the young technician **KES 30,400 to KES 58,000/month ($233 - $450 USD/mo)** in recurring middle-class income.

---

## 📊 Summary: Immediate Next Actions (Today & Tomorrow)

| Priority | Action Item | Where / Tool | Owner |
| :---: | :--- | :--- | :---: |
| 1️⃣ | Solder and wire the live bench demo rig (Pi Zero 2 + AI Camera + Amp + IMU). | Lab Bench | Engineering |
| 2️⃣ | Run `python3 apps/pi-client/test_hardware.py` & test live plate scanning. | Terminal | Engineering |
| 3️⃣ | Slice & 3D print the PETG enclosure parts. | ChipuRobo 3D Farm | ChipuRobo |
| 4️⃣ | Pitch the CEO at ChipuRobo tomorrow using [`IBORAIN_BUSINESS_MASTER_REPORT.md`](file:///Users/radebe49/smartB0t/IBORAIN_BUSINESS_MASTER_REPORT.md). | ChipuRobo Lab | Founder |
| 5️⃣ | Schedule the 14-day zero-CapEx pilot installation at Estate #1 (Syokimau). | Field / WhatsApp | Sales |
