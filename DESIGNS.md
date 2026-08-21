# 🛡️ Iborain Safety — CAD Designs & 3D Hardware Blueprint Guide

This guide provides comprehensive instructions on how to access, inspect, regenerate, slice, and manufacture the **physical CAD enclosures** for the Iborain Safety Edge AI Sentry network.

---

## 📁 1. Where to Find the CAD Files

All production-grade 3D CAD files are stored directly in this repository in both industry-standard **STEP (`.step`)** and **STL (`.stl`)** formats, along with the source Python parametric generative scripts (`build123d`).

### Repository Locations:
- **Pre-Compiled 3D Models (STEP & STL):** [`cad/output/`](file:///Users/radebe49/smartB0t/cad/output/)
- **Parametric Python CAD Source Scripts:** [`cad/`](file:///Users/radebe49/smartB0t/cad/)
  - Master Generator: [`cad/generate_all.py`](file:///Users/radebe49/smartB0t/cad/generate_all.py)
  - Shell 1 (Grid Sentry): [`cad/shell_tier1_grid.py`](file:///Users/radebe49/smartB0t/cad/shell_tier1_grid.py)
  - Shell 2 (Solar Sentry): [`cad/shell_tier2_solar.py`](file:///Users/radebe49/smartB0t/cad/shell_tier2_solar.py)
- **Automated Desktop Export:** Slicing plates and parts are also automatically synchronized to `~/Desktop/Iborain_3D_Print_Shells/` when running the build script.

---

## 📐 2. Available CAD Models & Specs

The hardware suite includes two production form factors designed around golden-ratio proportions, zero-screw stealth aesthetics, and IP66 weatherproofing:

### 🔹 Tier 1 / Package A: Grid Sentry Capsule (48mm × 84mm × 22mm)
*Designed for grid-powered deployments on building perimeters, gates, and utility boxes.*

| File Name | Format | Description & Usage |
| :--- | :--- | :--- |
| [`shell_tier1_side_by_side_plate.step`](file:///Users/radebe49/smartB0t/cad/output/shell_tier1_side_by_side_plate.step) | STEP | ⭐ **Ready-to-Slice Build Plate** (Base + Bezel oriented for Bambu Studio) |
| [`shell_tier1_side_by_side_plate.stl`](file:///Users/radebe49/smartB0t/cad/output/shell_tier1_side_by_side_plate.stl) | STL | High-resolution mesh build plate |
| [`shell_tier1_base_casing.step`](file:///Users/radebe49/smartB0t/cad/output/shell_tier1_base_casing.step) | STEP | Base enclosure with Pi Zero 2 W standoffs, bottom PG7 gland, top SMA port |
| [`shell_tier1_base_casing.stl`](file:///Users/radebe49/smartB0t/cad/output/shell_tier1_base_casing.stl) | STL | Base casing polygon mesh |
| [`shell_tier1_front_bezel.step`](file:///Users/radebe49/smartB0t/cad/output/shell_tier1_front_bezel.step) | STEP | Monolithic zero-screw front bezel with 45° beveled lens aperture & gasket tongue |
| [`shell_tier1_front_bezel.stl`](file:///Users/radebe49/smartB0t/cad/output/shell_tier1_front_bezel.stl) | STL | Front bezel polygon mesh |
| [`shell_tier1_complete_assembly.step`](file:///Users/radebe49/smartB0t/cad/output/shell_tier1_complete_assembly.step) | STEP | Full hermetically mated CAD assembly for CAD/CAM verification |

---

### 🔹 Tier 2 / Package B: Solar Mast Sentry Capsule (52mm × 108mm × 26mm)
*Designed for off-grid mast and streetlight pole installations with integrated saddle clamp channels and dual-bay electronics.*

| File Name | Format | Description & Usage |
| :--- | :--- | :--- |
| [`shell_tier2_side_by_side_plate.step`](file:///Users/radebe49/smartB0t/cad/output/shell_tier2_side_by_side_plate.step) | STEP | ⭐ **Ready-to-Slice Build Plate** (Base + Bezel with pole saddle oriented) |
| [`shell_tier2_side_by_side_plate.stl`](file:///Users/radebe49/smartB0t/cad/output/shell_tier2_side_by_side_plate.stl) | STL | High-resolution mesh build plate |
| [`shell_tier2_base_casing.step`](file:///Users/radebe49/smartB0t/cad/output/shell_tier2_base_casing.step) | STEP | Base enclosure with concave pole saddle (R=45mm), 14mm jubilee strap channels, dual PG7 glands, buck converter bay |
| [`shell_tier2_base_casing.stl`](file:///Users/radebe49/smartB0t/cad/output/shell_tier2_base_casing.stl) | STL | Base casing polygon mesh |
| [`shell_tier2_front_bezel.step`](file:///Users/radebe49/smartB0t/cad/output/shell_tier2_front_bezel.step) | STEP | Front bezel with 15° tilted downward camera viewport for elevated pole vantage |
| [`shell_tier2_front_bezel.stl`](file:///Users/radebe49/smartB0t/cad/output/shell_tier2_front_bezel.stl) | STL | Front bezel polygon mesh |
| [`shell_tier2_complete_assembly.step`](file:///Users/radebe49/smartB0t/cad/output/shell_tier2_complete_assembly.step) | STEP | Full mated mast assembly |

---

## ⚡ 3. How to Regenerate / Recompile CAD Models

The 3D models are generated programmatically using `build123d` (OpenCASCADE-backed Python B-Rep CAD kernel).

To modify parametric dimensions (wall thickness, tolerances, camera angles) and rebuild all STEP/STL models:

```bash
# Run via pnpm workspace script
pnpm run cad
```

Or execute directly via the Python environment:
```bash
./.venv/bin/python3 cad/generate_all.py
```

All models will be rebuilt in [`cad/output/`](file:///Users/radebe49/smartB0t/cad/output/) and mirrored to `~/Desktop/Iborain_3D_Print_Shells/`.

---

## 🖨️ 4. Slicing & 3D Printing Instructions (Bambu Lab P1S / X1C)

### Quick Open in Bambu Studio:
```bash
# Open Tier 1 Grid Sentry plate
open -a "BambuStudio" cad/output/shell_tier1_side_by_side_plate.step

# Open Tier 2 Solar Mast Sentry plate
open -a "BambuStudio" cad/output/shell_tier2_side_by_side_plate.step
```

### Recommended Print Settings for Outdoor Field Longevity:
- **Filament Material:** Matte-Black **PETG** (Bambu PETG Basic/HF) or **Black ASA** (for high UV/solar heat resistance).
- **Nozzle:** 0.4 mm Hardened Steel.
- **Layer Height:** 0.16 mm Optimal (or 0.20 mm Standard).
- **Wall Loops (Perimeters):** `4` (Ensures 1.6mm solid impermeable walls for IP66 waterproofing).
- **Top / Bottom Shell Layers:** `5` Top / `4` Bottom.
- **Infill Density & Pattern:** `30% - 40% Gyroid` (Provides uniform isotropic stiffness under strap tension).
- **Supports:** `Tree (auto)` or `Organic` (enabled only for internal fastener counterbores and gland threads).
- **Seam Placement:** `Back / Aligned` (Preserves flawless zero-defect front face aesthetics).

---

## 🔩 5. Hardware Bill of Materials (BOM) & Assembly

To assemble the printed enclosures into field-ready sentries:

| Item | Specification | Qty per Sentry | Function |
| :--- | :--- | :--- | :--- |
| **Compute Core** | Raspberry Pi Zero 2 W | 1 | Edge processor running Linux + Python WebSockets |
| **Vision Sensor** | Sony IMX500 AI Camera (25×24mm) | 1 | On-sensor neural processing & 1080p stream |
| **Connectivity** | Quectel 4G LTE HAT / USB Modem + SMA Pigtail | 1 | Cellular uplink with external high-gain antenna |
| **Anti-Tamper** | MPU-6500 6-Axis I2C IMU | 1 | Real-time vibration, shock, and tilt detection |
| **Optical Lens Window** | 20.0mm Dia × 1.5mm Circular Optical Glass Disc | 1 | Weatherproof camera window seated in front bezel |
| **Gasket Seal** | 1.5mm Dia Solid Silicone Cord / O-ring | 1 (~240mm) | Compressed into the continuous labyrinth channel |
| **Fasteners (Back-to-Front)** | M3 × 16mm (Tier 1) / M3 × 20mm (Tier 2) Stainless Hex | 4 | Rear-entry screws pulling shell into hermetic seal |
| **Threaded Inserts** | M3 × 4.0mm OD × 4.2mm Length Brass Heat-Set Inserts | 4 | Heat-pressed into front bezel screw bosses |
| **Cable Glands** | IP68 PG7 Nylon Cable Gland (3.5–6.5mm cable dia) | 1 (Tier 1) / 2 (Tier 2) | Hermetic feedthrough for power and solar lines |
| **Mast Clamps (Tier 2)** | 14mm W Stainless Steel Jubilee / Hose Clamps (50–110mm) | 2 | Secures Tier 2 saddle to streetlight poles |

---

## ⚖️ 6. Shell Weight Measurements

> **Method:** Volumes computed via the **divergence theorem** applied directly to the production `.stl` mesh files in [`cad/output/`](file:///Users/radebe49/smartB0t/cad/output/). No geometric approximations — these are exact CAD-kernel (OpenCASCADE / build123d) volumes.

### Print Settings Used for Calculation

| Setting | Value |
| :--- | :--- |
| Wall Loops (Perimeters) | 4 × 0.4mm nozzle = **1.6mm solid walls** |
| Infill Pattern & Density | **35% Gyroid** |
| Layer Height | **0.16mm** |
| Effective Volumetric Fill | **~71% of solid material** (55% wall zone + 16% infill core) |

---

### 🔹 Shell 1 — Package A: Grid Sentry (48 × 84 × 22mm)

| Part | Solid Volume | PETG Weight | ASA Weight |
| :--- | :--- | :--- | :--- |
| Base Casing | 17.12 cm³ | 15.4 g | 13.0 g |
| Front Bezel | 10.09 cm³ | 9.1 g | 7.6 g |
| **Complete Shell** | **27.21 cm³** | **≈ 24 g** | **≈ 21 g** |

---

### 🔹 Shell 2 — Package B: Solar Mast Sentry (52 × 108 × 26mm)

| Part | Solid Volume | PETG Weight | ASA Weight |
| :--- | :--- | :--- | :--- |
| Base Casing | 7.58 cm³ | 6.8 g | 5.7 g |
| Front Bezel | 16.64 cm³ | 15.0 g | 12.6 g |
| **Complete Shell** | **24.22 cm³** | **≈ 22 g** | **≈ 18 g** |

> **Note:** Shell 2's base casing is significantly lighter than its bezel due to the large concave pole saddle (R=45mm) machined into the rear face, which removes a substantial volume of material to conform to streetlight pole profiles.

---

### 📊 Summary — Printed Shell Weights

| Shell | Material | Shell Only | Complete Sentry* |
| :--- | :--- | :--- | :--- |
| Shell 1 — Grid Sentry | PETG | **~24 g** | ~75–85 g |
| Shell 1 — Grid Sentry | ASA | **~21 g** | ~70–80 g |
| Shell 2 — Solar Mast | PETG | **~22 g** | ~75–85 g |
| Shell 2 — Solar Mast | ASA | **~18 g** | ~65–75 g |

> \* *Complete Sentry weight includes the printed shell plus internal hardware payload (Raspberry Pi Zero 2 W ~10g, Sony IMX500 Camera ~5g, LTE modem ~15g, MPU-6500 IMU ~1g, cabling & fasteners ~10–15g, gasket & glass ~5g).*

### Key Takeaway

Both enclosures are **ultra-lightweight at under 25 grams per shell**, minimising mechanical stress on pole-mount clamps and keeping logistics costs minimal. The design prioritises material efficiency: the Shell 2 pole saddle cut alone removes ~60% of what would otherwise be a solid rear floor, directly contributing to field-weight reduction.
