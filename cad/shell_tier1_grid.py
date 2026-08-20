#!/usr/bin/env python3
"""
Iborain Safety — Ultra-Compact Stealth Jewel 3D CAD Generator for Shell 1 (Package A: Grid Sentry)
Design Philosophy: Minimalist Luxury Hardware (Tesla Autopilot Pillar / Apple / B&O Industrial Design)
  • Form Factor: Skin-Tight Monolithic Stadium Pill (38mm W x 74mm H x 18mm D) with R=10mm Fillets.
  • Part 1 (Rear Base Casing):
      - Skin-tight cavity holding Raspberry Pi Zero 2 W (65x30mm) on 4.0mm floor standoffs.
      - Integrated MPU-6500 Anti-Tamper IMU pocket.
      - Bottom-facing weatherproof cable entry port (dia 8.0mm) + top SMA 4G antenna port.
      - 2x Rear-entry M3 screw holes (concealed from front view for a 100% pristine front face).
      - Precision 1.4mm stepped labyrinth perimeter sealing rim (IP66).
  • Part 2 (Monolithic Front Bezel):
      - 100% Clean, pristine, zero-screw front face (zero protruding hoods, zero plastic noses).
      - Recessed 45° Beveled Optical Eye Window (dia 16.0mm) providing natural glare shielding.
      - Direct Sony IMX500 camera mounting standoffs on interior face (21.0mm x 12.5mm).
      - 2x M3 Brass Heat-Set Insert Bosses on the inside for rear fastening.

100% Pure Stealth: Ultra-Slim (18mm total depth), Pocketable, Monolithic, Zero Clutter.
"""
import os
import sys
from build123d import *

def build_tier1_base_casing():
    # Ultra-Compact Stadium Dimensions (mm)
    w, h, d = 38.0, 74.0, 15.5
    wall = 2.0
    floor_t = 2.0
    r = 10.0

    with BuildPart() as base:
        # 1. Skin-Tight Rounded Stadium Outer Envelope (z = 0 to d)
        with BuildSketch() as s1:
            Rectangle(w, h)
            fillet(s1.vertices(), radius=r)
        extrude(amount=d)

        # 2. Main Internal Compute Cavity (Hollowed to fit 65x30mm Pi Zero 2 W)
        with BuildSketch(Plane.XY.offset(floor_t)) as s2:
            Rectangle(w - 2 * wall, h - 2 * wall)
            fillet(s2.vertices(), radius=max(0.5, r - wall))
        extrude(amount=d - floor_t + 1.0, mode=Mode.SUBTRACT)

        # 3. 2x Rear Concealed Fastener Holes (M3 clearance holes entering from back z=0)
        with Locations([(0, -h/2 + 7.0, 0), (0, h/2 - 7.0, 0)]):
            Hole(radius=1.7, depth=floor_t + 2.0)
            # Recessed screw head well on the back
            with Locations((0, 0, 0)):
                Cylinder(radius=3.2, height=1.2, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        # 4. Raspberry Pi Zero 2 W Direct Floor Standoffs (58.0mm x 23.0mm)
        pi_center_y = 0.0
        pi_standoff_h = 3.5
        pi_offsets = [
            (-11.5, pi_center_y - 29.0),
            ( 11.5, pi_center_y - 29.0),
            ( 11.5, pi_center_y + 29.0),
            (-11.5, pi_center_y + 29.0),
        ]
        with Locations([(x, y, floor_t) for x, y in pi_offsets]):
            Cylinder(radius=2.4, height=pi_standoff_h, align=(Align.CENTER, Align.CENTER, Align.MIN))
            Hole(radius=1.1, depth=pi_standoff_h + 1.0) # M2.5 pilot

        # 5. MPU-6500 Anti-Tamper IMU Pocket
        with Locations((0, 0, floor_t)):
            Box(14.0, 18.0, 2.5, align=(Align.CENTER, Align.CENTER, Align.MIN))
            with Locations((0, -5.0, 2.5), (0, 5.0, 2.5)):
                Hole(radius=1.0, depth=2.5)

        # 6. Minimalist Weatherproof Ports
        # Bottom Face: 5V DC Power Cable Port (dia 8.0mm)
        with BuildSketch(Plane.XZ.offset(-h/2)):
            with Locations((0, floor_t + 6.0)):
                Circle(radius=4.0)
        extrude(amount=wall + 2.0, mode=Mode.SUBTRACT)

        # Top Face: SMA Antenna Port (dia 6.5mm)
        with BuildSketch(Plane.XZ.offset(h/2)):
            with Locations((0, floor_t + 6.0)):
                Circle(radius=3.25)
        extrude(amount=-(wall + 2.0), mode=Mode.SUBTRACT)

        # 7. Continuous Stepped Labyrinth Gasket Groove on Top Rim
        with BuildSketch(Plane.XY.offset(d)):
            Rectangle(w - wall, h - wall)
            fillet(s1.vertices(), radius=max(0.5, r - wall/2))
            Rectangle(w - wall - 1.8, h - wall - 1.8, mode=Mode.SUBTRACT)
        extrude(amount=-1.5, mode=Mode.SUBTRACT)

    return base.part


def build_tier1_front_bezel():
    # Monolithic Front Bezel Dimensions (mm)
    w, h, plate_t = 38.0, 74.0, 2.5
    r = 10.0
    cam_y = 12.0

    with BuildPart() as bezel:
        # 1. Smooth Stadium Front Faceplate (z = 0 to plate_t)
        with BuildSketch() as s:
            Rectangle(w, h)
            fillet(s.vertices(), radius=r)
        extrude(amount=plate_t)

        # 2. Recessed 45° Beveled Optical Eye Aperture (dia 16.0mm with 45° internal chamfer)
        with Locations((0, cam_y, 0)):
            Hole(radius=7.5, depth=plate_t + 2.0)
            # 45-degree chamfered lead-in for anti-glare shading
            with Locations((0, 0, plate_t - 1.0)):
                Cone(bottom_radius=9.0, top_radius=7.5, height=1.2, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        # 3. Direct Sony IMX500 Camera Mounting Grid on Interior (21.0mm x 12.5mm, z < 0)
        cam_offsets = [
            (-10.5, cam_y - 6.25),
            ( 10.5, cam_y - 6.25),
            ( 10.5, cam_y + 6.25),
            (-10.5, cam_y + 6.25),
        ]
        for x, y in cam_offsets:
            with Locations((x, y, 0)):
                Cylinder(radius=2.0, height=3.5, align=(Align.CENTER, Align.CENTER, Align.MAX))
                Hole(radius=0.9, depth=3.5) # M2 screw pilot

        # 4. 2x Concealed M3 Brass Heat-Set Insert Bosses on the Interior (z < 0)
        with Locations([(0, -h/2 + 7.0, 0), (0, h/2 - 7.0, 0)]):
            Cylinder(radius=3.8, height=6.0, align=(Align.CENTER, Align.CENTER, Align.MAX))
            Hole(radius=2.1, depth=6.0) # M3 brass insert pilot

        # 5. Continuous Perimeter Sealing Tongue (1.4mm W x 1.2mm H)
        with BuildSketch(Plane.XY):
            Rectangle(w - 2.0 - 0.4, h - 2.0 - 0.4)
            Rectangle(w - 2.0 - 1.8, h - 2.0 - 1.8, mode=Mode.SUBTRACT)
        extrude(amount=-1.2)

    return bezel.part


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out_dir, exist_ok=True)

    print("🛡️ Compiling Ultra-Compact Stealth Jewel Shell 1 (Package A: Grid Sentry)...")
    base = build_tier1_base_casing()
    bezel = build_tier1_front_bezel()

    export_step(base, os.path.join(out_dir, "shell_tier1_base_casing.step"))
    export_stl(base, os.path.join(out_dir, "shell_tier1_base_casing.stl"))
    export_step(bezel, os.path.join(out_dir, "shell_tier1_front_bezel.step"))
    export_stl(bezel, os.path.join(out_dir, "shell_tier1_front_bezel.stl"))

    # Complete Assembly
    assembly = Compound([
        base,
        bezel.moved(Location((0, 0, 15.5)))
    ])
    export_step(assembly, os.path.join(out_dir, "shell_tier1_complete_assembly.step"))
    print("  ✅ Shell 1 (38x74x18mm Ultra-Compact Stealth Jewel) Compiled Successfully!")
