#!/usr/bin/env python3
"""
Iborain Safety — Master 3D Print CAD Model Generator (Ultra-Slim 2-Piece Smooth Capsule System)
Generates and compiles production-ready .step & .stl models for:
  • Shell 1 (Package A: Grid Sentry Checkpoint — 76x78x27mm Pebble Capsule)
      - shell_tier1_base_casing.step / .stl
      - shell_tier1_front_bezel.step / .stl
      - shell_tier1_complete_assembly.step
  • Shell 2 (Package B: Solar Sentry Corridor — 94x114x35mm Stadium Capsule with Pole Saddle)
      - shell_tier2_base_casing.step / .stl
      - shell_tier2_front_bezel.step / .stl
      - shell_tier2_complete_assembly.step

Usage:
  pnpm run cad
  open -a "BambuStudio" cad/output/shell_tier1_complete_assembly.step
"""
import os
import sys
import shutil
import time

cad_dir = os.path.dirname(os.path.abspath(__file__))
if cad_dir not in sys.path:
    sys.path.insert(0, cad_dir)

t_start = time.time()

print("=" * 75)
print("  🛡️ Iborain Safety — Master 3D CAD Production Generator")
print("  Architecture: Ultra-Slim 2-Piece Smooth Capsule • Zero Loose Gaps")
print("  Target 3D Printer: Bambu Lab P1S (Matte-Black PETG / Black ASA)")
print("=" * 75)

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
# Shell 1: Grid Sentry (Ultra-Slim Pebble Capsule)
# -------------------------------------------------------------------------
print("\n[1/2] Compiling Shell 1: Package A (Grid Sentry Pebble Capsule)...")
t0 = time.time()
s1_base = build_tier1_base_casing()
s1_bezel = build_tier1_front_bezel()
s1_assy = Compound([
    s1_base,
    s1_bezel.moved(Location((0, 0, 24.0)))
])

export_step(s1_base, os.path.join(out_dir, "shell_tier1_base_casing.step"))
export_stl(s1_base, os.path.join(out_dir, "shell_tier1_base_casing.stl"))
export_step(s1_bezel, os.path.join(out_dir, "shell_tier1_front_bezel.step"))
export_stl(s1_bezel, os.path.join(out_dir, "shell_tier1_front_bezel.stl"))
export_step(s1_assy, os.path.join(out_dir, "shell_tier1_complete_assembly.step"))
print(f"  ✅ Shell 1 compiled in {time.time() - t0:.2f}s")

# -------------------------------------------------------------------------
# Shell 2: Solar Sentry (Streamlined Stadium Capsule)
# -------------------------------------------------------------------------
print("\n[2/2] Compiling Shell 2: Package B (Solar Sentry Stadium Capsule)...")
t0 = time.time()
s2_base = build_tier2_base_casing()
s2_bezel = build_tier2_front_bezel()
s2_assy = Compound([
    s2_base,
    s2_bezel.moved(Location((0, 0, 32.0)))
])

export_step(s2_base, os.path.join(out_dir, "shell_tier2_base_casing.step"))
export_stl(s2_base, os.path.join(out_dir, "shell_tier2_base_casing.stl"))
export_step(s2_bezel, os.path.join(out_dir, "shell_tier2_front_bezel.step"))
export_stl(s2_bezel, os.path.join(out_dir, "shell_tier2_front_bezel.stl"))
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
print("\n" + "=" * 75)
print("  🎉 All 2-Piece Smooth Capsule CAD Models Compiled Successfully!")
print(f"  Total Compilation Time: {time.time() - t_start:.2f}s")
print("=" * 75)
print("\nGenerated Models in `cad/output/` & on `~/Desktop/Iborain_3D_Print_Shells/`:")
for f in sorted(os.listdir(out_dir)):
    if f.startswith("."):
        continue
    fpath = os.path.join(out_dir, f)
    size_kb = os.path.getsize(fpath) / 1024
    print(f"  • {f:<44} ({size_kb:.1f} KB)")

print("\n🚀 Ready for Bambu Studio on your Mac:")
print("  open -a \"BambuStudio\" ~/Desktop/Iborain_3D_Print_Shells/shell_tier1_complete_assembly.step")
print("  open -a \"BambuStudio\" ~/Desktop/Iborain_3D_Print_Shells/shell_tier2_complete_assembly.step")
