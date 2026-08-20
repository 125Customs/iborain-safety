#!/usr/bin/env python3
"""
Iborain Safety — Ultra-Compact Stealth Mast Pod 3D CAD Generator for Shell 2 (Package B: Solar Sentry)
Design Philosophy: Minimalist Luxury Hardware (Tesla Autopilot / Apple / B&O Industrial Design)
  • Form Factor: Slim Vertical Stadium Pill (44mm W x 98mm H x 24mm D) with R=12mm Fillets.
  • Part 1 (Rear Base Casing with Pole Saddle):
      - Skin-tight dual-bay cavity holding Pi Zero 2 W (upper) and 12V buck regulator (lower).
      - Integrated Concave Pole Mount Contour (R=80mm) hugging utility poles flush.
      - Dual 12mm x 3.0mm Stainless Jubilee Strap Channels.
      - Dual bottom-facing weatherproof cable ports (Solar + Battery) & top SMA 4G port.
      - 4x Rear-entry M3 screw holes (concealed from front view for a 100% clean front face).
      - Precision 1.4mm stepped labyrinth perimeter sealing rim (IP66).
  • Part 2 (Monolithic Front Bezel):
      - 100% Clean, pristine, zero-screw front face (zero protruding hoods, zero plastic noses).
      - Recessed 15° Angled Beveled Optical Eye Window (dia 16.0mm) with anti-glare draft.
      - Direct Sony IMX500 camera mounting standoffs on interior face (21.0mm x 12.5mm).
      - 4x M3 Brass Heat-Set Insert Bosses on the inside for rear fastening.

100% Pure Stealth: Ultra-Slim (24mm total depth), Discreet Pole Mount, Monolithic Front Surface.
"""
import os
import sys
from build123d import *

def build_tier2_base_casing():
    # Ultra-Compact Stadium Dimensions (mm)
    w, h, d = 44.0, 98.0, 21.0
    wall = 2.2
    floor_t = 2.2
    r = 12.0

    with BuildPart() as base:
        # 1. Skin-Tight Rounded Stadium Outer Envelope
        with BuildSketch() as s1:
            Rectangle(w, h)
            fillet(s1.vertices(), radius=r)
        extrude(amount=d)

        # 2. Main Internal Dual-Bay Cavity
        with BuildSketch(Plane.XY.offset(floor_t)) as s2:
            Rectangle(w - 2 * wall, h - 2 * wall)
            fillet(s2.vertices(), radius=max(0.5, r - wall))
        extrude(amount=d - floor_t + 1.0, mode=Mode.SUBTRACT)

        # 3. Integrated Concave Pole Saddle on Rear Face (z = 0)
        with BuildSketch(Plane.YZ) as s_saddle:
            with Locations((0, -2.0)):
                Circle(40.0) # R=40mm radius (80mm diameter pole contour)
        extrude(amount=w + 2.0, both=True, mode=Mode.SUBTRACT)

        # 4. Dual 12mm Jubilee Strap Channels across the rear (Height 13mm, Depth 2.5mm)
        with Locations((0, 28.0, 0), (0, -28.0, 0)):
            Box(w + 4.0, 13.0, 2.5, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        # 5. 4x Rear-Entry M3 Fastener Holes (Concealed from front face)
        screw_positions = [
            (-w/2 + 6.0, -h/2 + 8.0, 0),
            ( w/2 - 6.0, -h/2 + 8.0, 0),
            ( w/2 - 6.0,  h/2 - 8.0, 0),
            (-w/2 + 6.0,  h/2 - 8.0, 0),
        ]
        with Locations(screw_positions):
            Hole(radius=1.7, depth=floor_t + 2.0)
            with Locations((0, 0, 0)):
                Cylinder(radius=3.2, height=1.2, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        # 6. Upper Bay: Raspberry Pi Zero 2 W Standoffs (58.0mm x 23.0mm)
        pi_center_y = 10.0
        pi_standoff_h = 3.5
        pi_offsets = [
            (-11.5, pi_center_y - 29.0),
            ( 11.5, pi_center_y - 29.0),
            ( 11.5, pi_center_y + 29.0),
            (-11.5, pi_center_y + 29.0),
        ]
        with Locations([(x, y, floor_t) for x, y in pi_offsets]):
            Cylinder(radius=2.4, height=pi_standoff_h, align=(Align.CENTER, Align.CENTER, Align.MIN))
            Hole(radius=1.1, depth=pi_standoff_h + 1.0)

        # 7. Lower Bay: 12V-to-5V Stepdown Buck Regulator Standoffs (32.0mm x 18.0mm)
        buck_center_y = -34.0
        buck_offsets = [
            (-9.0, buck_center_y - 12.0),
            ( 9.0, buck_center_y - 12.0),
            ( 9.0, buck_center_y + 12.0),
            (-9.0, buck_center_y + 12.0),
        ]
        with Locations([(x, y, floor_t) for x, y in buck_offsets]):
            Cylinder(radius=2.2, height=3.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
            Hole(radius=1.0, depth=3.0)

        # 8. Weatherproof Ingress Ports
        # Bottom Face: Dual Cable Ports (dia 7.0mm each) for Solar & Battery
        with BuildSketch(Plane.XZ.offset(-h/2)):
            with Locations((-10.0, floor_t + 7.0), (10.0, floor_t + 7.0)):
                Circle(radius=3.5)
        extrude(amount=wall + 2.0, mode=Mode.SUBTRACT)

        # Top Face: SMA Antenna Port (dia 6.5mm)
        with BuildSketch(Plane.XZ.offset(h/2)):
            with Locations((0, floor_t + 7.0)):
                Circle(radius=3.25)
        extrude(amount=-(wall + 2.0), mode=Mode.SUBTRACT)

        # 9. Continuous Stepped Labyrinth Gasket Groove on Top Rim
        with BuildSketch(Plane.XY.offset(d)):
            Rectangle(w - wall, h - wall)
            fillet(s1.vertices(), radius=max(0.5, r - wall/2))
            Rectangle(w - wall - 1.8, h - wall - 1.8, mode=Mode.SUBTRACT)
        extrude(amount=-1.5, mode=Mode.SUBTRACT)

    return base.part


def build_tier2_front_bezel():
    # Monolithic Front Bezel Dimensions (mm)
    w, h, plate_t = 44.0, 98.0, 3.0
    r = 12.0
    cam_y = 26.0

    with BuildPart() as bezel:
        # 1. Smooth Stadium Front Faceplate (z = 0 to plate_t)
        with BuildSketch() as s:
            Rectangle(w, h)
            fillet(s.vertices(), radius=r)
        extrude(amount=plate_t)

        # 2. Recessed 15° Angled Beveled Optical Eye Aperture (dia 16.0mm)
        with Locations((0, cam_y, 0)):
            Hole(radius=7.5, depth=plate_t + 2.0)
            with Locations((0, 0, plate_t - 1.2)):
                Cone(bottom_radius=9.5, top_radius=7.5, height=1.4, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        # 3. Direct Sony IMX500 Camera Mounting Grid on Interior (21.0mm x 12.5mm, z < 0)
        cam_offsets = [
            (-10.5, cam_y - 6.25),
            ( 10.5, cam_y - 6.25),
            ( 10.5, cam_y + 6.25),
            (-10.5, cam_y + 6.25),
        ]
        for x, y in cam_offsets:
            with Locations((x, y, 0)):
                Cylinder(radius=2.2, height=4.0, align=(Align.CENTER, Align.CENTER, Align.MAX))
                Hole(radius=1.0, depth=4.0)

        # 4. 4x Concealed M3 Brass Heat-Set Insert Bosses on Interior (z < 0)
        screw_positions = [
            (-w/2 + 6.0, -h/2 + 8.0, 0),
            ( w/2 - 6.0, -h/2 + 8.0, 0),
            ( w/2 - 6.0,  h/2 - 8.0, 0),
            (-w/2 + 6.0,  h/2 - 8.0, 0),
        ]
        for x, y, _ in screw_positions:
            with Locations((x, y, 0)):
                Cylinder(radius=3.8, height=6.0, align=(Align.CENTER, Align.CENTER, Align.MAX))
                Hole(radius=2.1, depth=6.0)

        # 5. Continuous Perimeter Sealing Tongue (1.4mm W x 1.2mm H)
        with BuildSketch(Plane.XY):
            Rectangle(w - 2.2 - 0.4, h - 2.2 - 0.4)
            Rectangle(w - 2.2 - 1.8, h - 2.2 - 1.8, mode=Mode.SUBTRACT)
        extrude(amount=-1.2)

    return bezel.part


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out_dir, exist_ok=True)

    print("🛡️ Compiling Ultra-Compact Stealth Mast Pod Shell 2 (Package B: Solar Sentry)...")
    base = build_tier2_base_casing()
    bezel = build_tier2_front_bezel()

    export_step(base, os.path.join(out_dir, "shell_tier2_base_casing.step"))
    export_stl(base, os.path.join(out_dir, "shell_tier2_base_casing.stl"))
    export_step(bezel, os.path.join(out_dir, "shell_tier2_front_bezel.step"))
    export_stl(bezel, os.path.join(out_dir, "shell_tier2_front_bezel.stl"))

    # Complete Assembly
    assembly = Compound([
        base,
        bezel.moved(Location((0, 0, 21.0)))
    ])
    export_step(assembly, os.path.join(out_dir, "shell_tier2_complete_assembly.step"))
    print("  ✅ Shell 2 (44x98x24mm Ultra-Compact Stealth Mast Pod) Compiled Successfully!")
