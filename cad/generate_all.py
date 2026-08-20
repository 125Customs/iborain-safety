#!/usr/bin/env python3
"""
Iborain Safety — Master 3D Print CAD Model Generator (Sentry-Core™ Sled Architecture)
Generates and compiles production-ready .step & .stl models for:
  • Shell 1 (Package A: Grid Sentry Checkpoint Enclosure)
      - shell_tier1_exoskeleton.step / .stl
      - shell_tier1_carrier_sled.step / .stl
      - shell_tier1_faceplate_visor.step / .stl
      - shell_tier1_complete_assembly.step
  • Shell 2 (Package B: Solar Sentry Corridor Pole-Mount Enclosure)
      - shell_tier2_exoskeleton.step / .stl
      - shell_tier2_carrier_sled.step / .stl
      - shell_tier2_faceplate_visor.step / .stl
      - shell_tier2_complete_assembly.step

Usage:
  pnpm run cad
  open -a "BambuStudio" cad/output/shell_tier1_complete_assembly.step
"""
import os
import sys
import time

cad_dir = os.path.dirname(os.path.abspath(__file__))
if cad_dir not in sys.path:
    sys.path.insert(0, cad_dir)

t_start = time.time()

print("=" * 75)
print("  🛡️ Iborain Safety — Master 3D CAD Production Generator (Sentry-Core™)")
print("  Design Language: Cyber-Stealth Facets • Zero-Gap Sled • Hermetic Seal")
print("  Target 3D Printer: Bambu Lab P1S (Matte-Black PETG / Black ASA)")
print("=" * 75)

from shell_tier1_grid import (
    build_tier1_exoskeleton,
    build_tier1_carrier_sled,
    build_tier1_faceplate_visor
)
from shell_tier2_solar import (
    build_tier2_exoskeleton,
    build_tier2_carrier_sled,
    build_tier2_faceplate_visor
)
from build123d import Compound, Location, export_step, export_stl

out_dir = os.path.join(cad_dir, "output")
os.makedirs(out_dir, exist_ok=True)

# -------------------------------------------------------------------------
# Shell 1: Grid Sentry Checkpoint Enclosure
# -------------------------------------------------------------------------
print("\n[1/2] Compiling Shell 1: Package A (Grid Sentry Checkpoint)...")
t0 = time.time()
s1_exo = build_tier1_exoskeleton()
s1_sled = build_tier1_carrier_sled()
s1_bezel = build_tier1_faceplate_visor()
s1_assy = Compound([
    s1_exo,
    s1_sled.moved(Location((0, 0, 3.0))),
    s1_bezel.moved(Location((0, 0, 40.0)))
])

export_step(s1_exo, os.path.join(out_dir, "shell_tier1_exoskeleton.step"))
export_stl(s1_exo, os.path.join(out_dir, "shell_tier1_exoskeleton.stl"))
export_step(s1_sled, os.path.join(out_dir, "shell_tier1_carrier_sled.step"))
export_stl(s1_sled, os.path.join(out_dir, "shell_tier1_carrier_sled.stl"))
export_step(s1_bezel, os.path.join(out_dir, "shell_tier1_faceplate_visor.step"))
export_stl(s1_bezel, os.path.join(out_dir, "shell_tier1_faceplate_visor.stl"))
export_step(s1_assy, os.path.join(out_dir, "shell_tier1_complete_assembly.step"))
print(f"  ✅ Shell 1 compiled in {time.time() - t0:.2f}s")

# -------------------------------------------------------------------------
# Shell 2: Solar Sentry Corridor Pole-Mount Enclosure
# -------------------------------------------------------------------------
print("\n[2/2] Compiling Shell 2: Package B (Solar Sentry Corridor Pole-Mount)...")
t0 = time.time()
s2_exo = build_tier2_exoskeleton()
s2_sled = build_tier2_carrier_sled()
s2_bezel = build_tier2_faceplate_visor()
s2_assy = Compound([
    s2_exo,
    s2_sled.moved(Location((0, 0, 3.5))),
    s2_bezel.moved(Location((0, 0, 54.0)))
])

export_step(s2_exo, os.path.join(out_dir, "shell_tier2_exoskeleton.step"))
export_stl(s2_exo, os.path.join(out_dir, "shell_tier2_exoskeleton.stl"))
export_step(s2_sled, os.path.join(out_dir, "shell_tier2_carrier_sled.step"))
export_stl(s2_sled, os.path.join(out_dir, "shell_tier2_carrier_sled.stl"))
export_step(s2_bezel, os.path.join(out_dir, "shell_tier2_faceplate_visor.step"))
export_stl(s2_bezel, os.path.join(out_dir, "shell_tier2_faceplate_visor.stl"))
export_step(s2_assy, os.path.join(out_dir, "shell_tier2_complete_assembly.step"))
print(f"  ✅ Shell 2 compiled in {time.time() - t0:.2f}s")

# -------------------------------------------------------------------------
# Summary Report
# -------------------------------------------------------------------------
print("\n" + "=" * 75)
print("  🎉 All Premium Sentry-Core™ CAD Models Compiled Successfully!")
print(f"  Total Compilation Time: {time.time() - t_start:.2f}s")
print("=" * 75)
print("\nGenerated Models in `cad/output/`:")
for f in sorted(os.listdir(out_dir)):
    if f.startswith(".") or f.startswith("test_"):
        continue
    fpath = os.path.join(out_dir, f)
    size_kb = os.path.getsize(fpath) / 1024
    print(f"  • {f:<44} ({size_kb:.1f} KB)")

print("\n🚀 Ready for Bambu Studio on your Mac:")
print("  open -a \"BambuStudio\" cad/output/shell_tier1_complete_assembly.step")
print("  open -a \"BambuStudio\" cad/output/shell_tier2_complete_assembly.step")
