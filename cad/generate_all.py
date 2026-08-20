#!/usr/bin/env python3
"""
Iborain Safety — Master 3D Print CAD Model Generator
Generates and compiles production-ready .step & .stl models for:
  • Shell 1 (Package A: Grid Sentry Checkpoint Enclosure)
  • Shell 2 (Package B: Solar Sentry Corridor Pole-Mount Enclosure)

Usage:
  pnpm run cad
  python3 cad/generate_all.py
"""
import os
import sys
import time

cad_dir = os.path.dirname(os.path.abspath(__file__))
if cad_dir not in sys.path:
    sys.path.insert(0, cad_dir)

t_start = time.time()

print("=" * 70)
print("  🛡️ Iborain Safety — Master 3D CAD Production Generator")
print("  Target 3D Printer: Bambu Lab P1S (Matte-Black PETG / ASA)")
print("=" * 70)

from shell_tier1_grid import build_tier1_main_box, build_tier1_faceplate
from shell_tier2_solar import build_tier2_main_box, build_tier2_faceplate
from build123d import Compound, Location, export_step, export_stl

out_dir = os.path.join(cad_dir, "output")
os.makedirs(out_dir, exist_ok=True)

# -------------------------------------------------------------------------
# Shell 1: Grid Sentry
# -------------------------------------------------------------------------
print("\n[1/2] Compiling Shell 1 (Package A: Grid Sentry Checkpoint)...")
t0 = time.time()
s1_box = build_tier1_main_box()
s1_face = build_tier1_faceplate()
s1_assy = Compound([s1_box, s1_face.moved(Location((0, 0, 36.0)))])

export_step(s1_box, os.path.join(out_dir, "shell_tier1_main_box.step"))
export_stl(s1_box, os.path.join(out_dir, "shell_tier1_main_box.stl"))
export_step(s1_face, os.path.join(out_dir, "shell_tier1_faceplate_visor.step"))
export_stl(s1_face, os.path.join(out_dir, "shell_tier1_faceplate_visor.stl"))
export_step(s1_assy, os.path.join(out_dir, "shell_tier1_complete_assembly.step"))
print(f"  ✅ Shell 1 compiled in {time.time() - t0:.2f}s")

# -------------------------------------------------------------------------
# Shell 2: Solar Sentry
# -------------------------------------------------------------------------
print("\n[2/2] Compiling Shell 2 (Package B: Solar Sentry Corridor Pole-Mount)...")
t0 = time.time()
s2_box = build_tier2_main_box()
s2_face = build_tier2_faceplate()
s2_assy = Compound([s2_box, s2_face.moved(Location((0, 0, 50.0)))])

export_step(s2_box, os.path.join(out_dir, "shell_tier2_main_box.step"))
export_stl(s2_box, os.path.join(out_dir, "shell_tier2_main_box.stl"))
export_step(s2_face, os.path.join(out_dir, "shell_tier2_faceplate_visor.step"))
export_stl(s2_face, os.path.join(out_dir, "shell_tier2_faceplate_visor.stl"))
export_step(s2_assy, os.path.join(out_dir, "shell_tier2_complete_assembly.step"))
print(f"  ✅ Shell 2 compiled in {time.time() - t0:.2f}s")

# -------------------------------------------------------------------------
# Summary Report
# -------------------------------------------------------------------------
print("\n" + "=" * 70)
print("  🎉 All 3D CAD Production Models Compiled Successfully!")
print(f"  Total Compilation Time: {time.time() - t_start:.2f}s")
print("=" * 70)
print("\nGenerated Models in `cad/output/`:")
for f in sorted(os.listdir(out_dir)):
    if f.startswith(".") or f.startswith("test_"):
        continue
    fpath = os.path.join(out_dir, f)
    size_kb = os.path.getsize(fpath) / 1024
    print(f"  • {f:<42} ({size_kb:.1f} KB)")

print("\n🚀 To open models directly in Bambu Studio on your Mac:")
print("  open -a \"BambuStudio\" cad/output/shell_tier1_main_box.step")
print("  open -a \"BambuStudio\" cad/output/shell_tier1_faceplate_visor.step")
print("  open -a \"BambuStudio\" cad/output/shell_tier2_main_box.step")
print("  open -a \"BambuStudio\" cad/output/shell_tier2_faceplate_visor.step")
