#!/usr/bin/env python3
"""
Iborain Safety — Master 3D Print CAD Model Generator (Flipped & Print-Optimized Plates)
Generates and compiles production-ready .step & .stl models for Bambu Lab P1S:

  1. Shell 1 (Package A: Grid Sentry 76x80x26mm Pebble Capsule)
     • ⭐ shell_tier1_side_by_side_plate.step / .stl  [FLIPPED FOR OPTIMAL PRINTING - ZERO SUPPORTS]
     • shell_tier1_base_casing.step / .stl
     • shell_tier1_front_bezel.step / .stl            [PRE-FLIPPED FLAT ON BED]
     • shell_tier1_complete_assembly.step             [CLOSED CAD ASSEMBLY]

  2. Shell 2 (Package B: Solar Sentry 92x116x34mm Stadium Capsule with Pole Saddle)
     • ⭐ shell_tier2_side_by_side_plate.step / .stl  [FLIPPED FOR OPTIMAL PRINTING - ZERO SUPPORTS]
     • shell_tier2_base_casing.step / .stl
     • shell_tier2_front_bezel.step / .stl            [PRE-FLIPPED FLAT ON BED]
     • shell_tier2_complete_assembly.step             [CLOSED CAD ASSEMBLY]

Usage:
  pnpm run cad
  open -a "BambuStudio" ~/Desktop/Iborain_3D_Print_Shells/shell_tier1_side_by_side_plate.step
"""
import os
import sys
import shutil
import time

cad_dir = os.path.dirname(os.path.abspath(__file__))
if cad_dir not in sys.path:
    sys.path.insert(0, cad_dir)

t_start = time.time()

print("=" * 80)
print("  🛡️ Iborain Safety — Master 3D CAD Production Generator (Print-Flipped Plates)")
print("  Optimization: Umbrella Component Flipped Flat on Bed • Zero Support Requirement")
print("  Target 3D Printer: Bambu Lab P1S (Matte-Black PETG / Black ASA)")
print("=" * 80)

from shell_tier1_grid import (
    build_tier1_base_casing,
    build_tier1_front_bezel
)
from shell_tier2_solar import (
    build_tier2_base_casing,
    build_tier2_front_bezel
)
from build123d import Compound, Location, export_step, export_stl

out_dir = os.path.join(cad_dir, "output")
os.makedirs(out_dir, exist_ok=True)

# -------------------------------------------------------------------------
# Shell 1: Grid Sentry (Pebble Capsule)
# -------------------------------------------------------------------------
print("\n[1/2] Compiling Shell 1: Package A (Grid Sentry Pebble Capsule)...")
t0 = time.time()
s1_base = build_tier1_base_casing()
s1_bezel_raw = build_tier1_front_bezel()

# Flip the front bezel 180° around X axis and align bottom to Z=0 for flawless bed adhesion
s1_bezel_flipped = s1_bezel_raw.moved(Location((0, 0, 0), (180, 0, 0)))
s1_bezel_print_ready = s1_bezel_flipped.moved(Location((0, 0, -s1_bezel_flipped.bounding_box().min.Z)))

# 1. Side-by-Side Ready-to-Slice Build Plate (Base on left, Flipped Bezel on right)
s1_plate = Compound([
    s1_base.moved(Location((-48.0, 0, 0))),
    s1_bezel_print_ready.moved(Location(( 48.0, 0, 0)))
])
export_step(s1_plate, os.path.join(out_dir, "shell_tier1_side_by_side_plate.step"))
export_stl(s1_plate, os.path.join(out_dir, "shell_tier1_side_by_side_plate.stl"))

# 2. Individual Parts
export_step(s1_base, os.path.join(out_dir, "shell_tier1_base_casing.step"))
export_stl(s1_base, os.path.join(out_dir, "shell_tier1_base_casing.stl"))
export_step(s1_bezel_print_ready, os.path.join(out_dir, "shell_tier1_front_bezel.step"))
export_stl(s1_bezel_print_ready, os.path.join(out_dir, "shell_tier1_front_bezel.stl"))

# 3. Closed Assembly (for CAD inspection)
s1_assy = Compound([
    s1_base,
    s1_bezel_raw.moved(Location((0, 0, 23.0)))
])
export_step(s1_assy, os.path.join(out_dir, "shell_tier1_complete_assembly.step"))
print(f"  ✅ Shell 1 compiled in {time.time() - t0:.2f}s")

# -------------------------------------------------------------------------
# Shell 2: Solar Sentry (Stadium Capsule with Pole Saddle)
# -------------------------------------------------------------------------
print("\n[2/2] Compiling Shell 2: Package B (Solar Sentry Stadium Capsule)...")
t0 = time.time()
s2_base = build_tier2_base_casing()
s2_bezel_raw = build_tier2_front_bezel()

# Flip Shell 2 bezel 180° around X axis and align bottom to Z=0
s2_bezel_flipped = s2_bezel_raw.moved(Location((0, 0, 0), (180, 0, 0)))
s2_bezel_print_ready = s2_bezel_flipped.moved(Location((0, 0, -s2_bezel_flipped.bounding_box().min.Z)))

# 1. Side-by-Side Ready-to-Slice Build Plate (Base on left, Flipped Bezel on right)
s2_plate = Compound([
    s2_base.moved(Location((-60.0, 0, 0))),
    s2_bezel_print_ready.moved(Location(( 60.0, 0, 0)))
])
export_step(s2_plate, os.path.join(out_dir, "shell_tier2_side_by_side_plate.step"))
export_stl(s2_plate, os.path.join(out_dir, "shell_tier2_side_by_side_plate.stl"))

# 2. Individual Parts
export_step(s2_base, os.path.join(out_dir, "shell_tier2_base_casing.step"))
export_stl(s2_base, os.path.join(out_dir, "shell_tier2_base_casing.stl"))
export_step(s2_bezel_print_ready, os.path.join(out_dir, "shell_tier2_front_bezel.step"))
export_stl(s2_bezel_print_ready, os.path.join(out_dir, "shell_tier2_front_bezel.stl"))

# 3. Closed Assembly
s2_assy = Compound([
    s2_base,
    s2_bezel_raw.moved(Location((0, 0, 32.0)))
])
export_step(s2_assy, os.path.join(out_dir, "shell_tier2_complete_assembly.step"))
print(f"  ✅ Shell 2 compiled in {time.time() - t0:.2f}s")

# Copy directly to user's Desktop folder
desktop_dir = os.path.expanduser("~/Desktop/Iborain_3D_Print_Shells")
os.makedirs(desktop_dir, exist_ok=True)
for f in os.listdir(out_dir):
    if not f.startswith("."):
        shutil.copy2(os.path.join(out_dir, f), os.path.join(desktop_dir, f))

# -------------------------------------------------------------------------
# Summary Report
# -------------------------------------------------------------------------
print("\n" + "=" * 80)
print("  🎉 All 3D CAD Print-Flipped Models Compiled Successfully!")
print(f"  Total Compilation Time: {time.time() - t_start:.2f}s")
print("=" * 80)
print("\nGenerated Models in `cad/output/` & on `~/Desktop/Iborain_3D_Print_Shells/`:")
for f in sorted(os.listdir(out_dir)):
    if f.startswith("."):
        continue
    fpath = os.path.join(out_dir, f)
    size_kb = os.path.getsize(fpath) / 1024
    star = "⭐ [READY-TO-SLICE]" if "side_by_side" in f else "  "
    print(f"  {star} {f:<44} ({size_kb:.1f} KB)")

print("\n🚀 Ready for Bambu Studio on your Mac:")
print("  open -a \"BambuStudio\" ~/Desktop/Iborain_3D_Print_Shells/shell_tier1_side_by_side_plate.step")
print("  open -a \"BambuStudio\" ~/Desktop/Iborain_3D_Print_Shells/shell_tier2_side_by_side_plate.step")
