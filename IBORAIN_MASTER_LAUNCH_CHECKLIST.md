# 🚀 Iborain Safety — Master Launch, Fabrication & Sales Execution Checklist
*The 100% Pure Stealth Architecture: Zero Lights, Zero Screens, Pure Optical Intelligence*

**Company:** Iborain Safety Ltd. (Nairobi, Kenya)  
**Fabrication Hub:** [ChipuRobo STEM Makerspaces](https://chipurobo.com/)  
**Hardware Philosophy:** Completely Stealth Black-Box Sentry (Raspberry Pi Zero 2 W + Sony IMX500 AI Camera + 4G LTE + MPU-6500 Anti-Tamper)

---

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 THE 6-PHASE MASTER LAUNCH ROADMAP                                │
├────────────────────────────────┬─────────────────────────────────────────────────────────────────┤
│ 🟢 Phase 1: Bench Demo Rig     │ Solder pure 3-chip perfboard (Pi Zero 2 + IMX500 + IMU).        │
├────────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ 🔵 Phase 2: 3D Print Packaging │ Single-lens stealth enclosure (zero LED holes, zero screen cuts)│
├────────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ 🟣 Phase 3: Cloud & Web Infra  │ Deploy Cloud Run broker, Next.js site, M-Pesa & WhatsApp.       │
├────────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ 🟡 Phase 4: Field Calibration  │ Optical telephoto focus (3-10m), 4G LTE cellular soak test.     │
├────────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ 🔴 Phase 5: 14-Day Pilot Sales │ Deploy Package A to estates at $49/mo (14-day free trial).      │
├────────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ 🟠 Phase 6: CCTV SaaS Upsell   │ Onboard hospitals & malls at $20/camera/mo (91% profit margin). │
└────────────────────────────────┴─────────────────────────────────────────────────────────────────┘
```

---

## 🟢 PHASE 1: The Bench Demo & Live Scanning Rig (Do This First)

*Objective: Assemble your streamlined 3-chip physical electronics on a clean perfboard and verify live multimodal scanning with Google Gemini.*

### 1.1 Physical Hardware Soldering & Wiring (Pure 2-Chip Core)
- [ ] **Mount Raspberry Pi Zero 2 W:** Solder male 40-pin GPIO header pins.
- [ ] **Connect Vision Sensor:** Attach the Sony IMX500 AI Camera ribbon cable to the CSI camera port (blue stiffener tab facing the board). Senses vehicle/boda arrivals autonomously via on-sensor Neural ROI at 30 fps.
- [ ] **Wire Anti-Tamper & Anti-Theft Sensor (MPU-6500 6-Axis IMU):**
  - [ ] Connect `SDA` to Raspberry Pi `GPIO 2` (Pin 3).
  - [ ] Connect `SCL` to Raspberry Pi `GPIO 3` (Pin 5).
  - [ ] Connect `VCC` to `3.3V Rail` (Pin 1).
  - [ ] Connect `GND` to `Common Ground` (Pin 9).

```
                              ┌─────────────────────────┐
                              │  Raspberry Pi Zero 2 W  │
                 3.3V Power ──┤ [1]  (3V3)    (5V)  [2] ├── 5V Power In (from Buck/Adapter)
     (I2C SDA -> MPU-6500) ───┤ [3]  (GPIO2)  (5V)  [4] │
     (I2C SCL -> MPU-6500) ───┤ [5]  (GPIO3)  (GND) [6] ├── Common Ground
                              │ [7]  (GPIO4)  (TXD) [8] │
                 Common GND ──┤ [9]  (GND)    (RXD) [10]│
                              │ [11] (GPIO17) (IO18)[12]│
                              │ [13] (GPIO27) (GND) [14]│
                              │ [15] (GPIO22) (IO23)[16]│
                 3.3V Power ──┤ [17] (3V3)    (IO24)[18]│
                              │ [19] (MOSI)   (GND) [20]│
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
  - [ ] Verify camera capture detects Sony IMX500.
- [ ] **Live Gemini Vision Loop Verification:**
  - [ ] Start Cloud Run or local broker: `MODE=gemini pnpm run dev:backend`.
  - [ ] Launch edge client: `python3 apps/pi-client/robot.py --url ws://localhost:8080/ws/device`.
  - [ ] Hold up printed license plate `KDA 482B` or Boda Boda photo $\rightarrow$ verify Gemini returns transit fingerprint in sub-600ms and sends WhatsApp alert.

---

## 🔵 PHASE 2: 3D Printing & Enclosure Packaging (At ChipuRobo)

*Objective: Fabricate a 100% stealth, single-lens weatherproof outdoor enclosure with zero visible light apertures.*

### 2.1 3D CAD & Slicing Setup
- [ ] **Material:** **Black PETG or ASA** (UV-resistant, matte finish for stealth).
- [ ] **Print Settings:** 0.20mm layer height, 4 outer walls, 25% Gyroid infill.
- [ ] **Print Component 1 (Main Casing Box):** Compact enclosure housing Pi Zero 2, IMU, and 4G modem.
- [ ] **Print Component 2 (Front Faceplate):** Single 20mm camera lens aperture only. (Zero LED holes, zero display cutouts).
- [ ] **Print Component 3 (Sun/Rain Visor Hood):** 25mm overhang hood protecting lens from direct rain and sunlight glare.
- [ ] **Print Component 4 (Universal Pole Mount):** Curved rear bracket with dual 15mm slots for stainless jubilee hose clamps.

---

## 🟣 PHASE 3: Production Cloud & Web Infrastructure Deployment

*Objective: Launch the public web presence, Google Cloud Run backend, WhatsApp dispatch webhook, and M-Pesa billing engine.*

### 3.1 Google Cloud Run Backend (`apps/backend`)
- [ ] Set environment secrets in Google Secret Manager (`GEMINI_API_KEY`, `DEVICE_AUTH_TOKENS`, `WHATSAPP_TOKEN`).
- [ ] Execute automated deployment: `GCP_PROJECT=your-project-id MODE=gemini bash apps/backend/deploy.sh`.
- [ ] Verify live WebSocket URL: `wss://iborain-broker-<hash>.a.run.app/ws/device`.

### 3.2 Public Web Landing Page (`apps/landing`)
- [ ] Build Next.js application: `cd apps/landing && pnpm build`.
- [ ] Deploy to production hosting on custom domain (`iborain.com` / `iborainsafety.com`).
- [ ] Verify pricing matrix: **Package A ($49/mo)**, **Package B ($99/mo)**, and **Package C ($20/cam/mo)**.

### 3.3 WhatsApp Business & M-Pesa Daraja Integration
- [ ] **WhatsApp Cloud API:** Configure webhook to dispatch instant JSON alert payloads (Photo proof + Plate + Cargo) directly to registered security group chats in under 1 second.
- [ ] **M-Pesa Daraja API:** Configure automated STK Push recurring billing scheduled for the 1st of every month.

---

## 🟡 PHASE 4: Field Testing & Optical Calibration

*Objective: Calibrate camera focus and cellular reliability in realistic outdoor conditions.*

### 4.1 Optical & Scene Calibration
- [ ] **Focal Distance:** Adjust telephoto lens focus at **3 meters, 6 meters, and 10 meters** for maximum plate sharpness.
- [ ] **Angle Optimization:** Set mounting pitch to **15° downward tilt** to eliminate oncoming headlight glare.

### 4.2 Cellular & Network Resilience
- [ ] **SIM Card Activation:** Install Safaricom/Airtel IoT SIM card with active 4G data bundle.
- [ ] **24-Hour Soak Test:** Run continuous edge client connected to Cloud Run broker for 24 hours over 4G.
- [ ] **Fault Recovery:** Disconnect antenna $\rightarrow$ verify unit buffers logs locally in SQLite and auto-reconnects within 5 seconds of signal restoration.

---

## 🔴 PHASE 5: The 14-Day Pilot Customer Rollout (Selling to Estates)

*Objective: Deploy Package A (Grid Sentry) to your 3 pilot estate security committees and convert them into paying monthly subscriptions.*

### 5.1 The Chairman Pitch & Agreement
- [ ] **Target:** Meet with Estate Security Committee Chairman & Treasurer (e.g. Syokimau Court, Ruiru Gated Court, Membley).
- [ ] **The Offer:** *"We install the complete Iborain Safety system at your gate today for KES 0 upfront. Test it for 14 days. If your residents don't love the instant WhatsApp clearance and security alerts, we take it down for free."*
- [ ] **Execute Pilot Agreement:** Sign the 14-Day Zero-CapEx Safety Lease Pilot Form.

### 5.2 On-Site Gate Installation (Takes 15 Minutes)
- [ ] **Mounting:** Strap enclosure securely to barrier post or light pole at **2.4 meters height** using stainless steel jubilee straps.
- [ ] **Power:** Plug 5V/3A power adapter into gatehouse AC outlet.
- [ ] **Group Setup:** Create official estate security WhatsApp group (add Estate Chairman, Security Committee, and Head Guard).

### 5.3 Day 1 to 14 Pilot Monitoring & Conversion
- [ ] **Day 7 Mid-Pilot Report:** Send an automated 1-page PDF summary to the Estate Chairman showing total vehicles fingerprinted.
- [ ] **Day 14 Final Conversion:** Sign 12-month recurring contract (**KES 6,500/month**) via automated M-Pesa STK Push.

---

## 🟠 PHASE 6: Scaling Package C (Smart CCTV Cloud at $20/Camera/Mo)

*Objective: Onboard hospitals, malls, and enterprise facilities with existing CCTV cameras at 91% pure profit margin.*

### 6.1 The Hospital / Mall Pitch
- [ ] **Target:** Head of Security at Kenyatta National Hospital, Aga Khan, MP Shah, Sarit Centre, Two Rivers.
- [ ] **The Pitch:** *"Turn your existing 20+ Hikvision/Dahua CCTV cameras into real-time AI sentries. Instant WhatsApp threat detection and natural language crime search for only $20/camera/month with ZERO new hardware to buy."*
- [ ] **Integration:** Connect existing NVR RTSP stream URLs to Iborain Cloud Run.
- [ ] **Financial Yield:** 25 connected cameras generate **$500/month (KES 65,000/mo)** with **$455/mo in net profit**!
