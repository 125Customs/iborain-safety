#!/usr/bin/env python3
"""
Iborain Safety — Desert-Grade Aerodynamic Bullet Pod 3D CAD Generator for Shell 2 (Package B: Solar Sentry)
Design Language: Smooth Stadium Capsule / 15° Angled Semicircular Bulging Umbrella Hood
  1. Base Casing: Aerodynamic 24mm-radius stadium body with integrated rear pole saddle (100mm radius),
     dual 15mm Jubilee clamp slots, direct Pi Zero 2 W + 12V buck regulator standoffs, dual PG7 ports & SMA port.
  2. Front Bezel & Umbrella Visor: Streamlined front plate with integrated 15° angled semicircular
     umbrella hood (R=18mm arch), 20.4mm optical aperture, and direct Sony IMX500 camera mounting standoffs.

100% Pure Stealth: Aerodynamic Dust-Shedding Silhouette, Smooth Double Curves, Zero Loose Gaps.
"""
import os
import sys
from build123d import *

def build_tier2_base_casing():
    # Stadium Capsule Dimensions (mm)
    w, h, d = 92.0, 116.0, 32.0
    wall = 2.6
    floor_t = 2.8
    r = 24.0

    with BuildPart() as base:
        # 1. Smooth Stadium Rounded Envelope
        with BuildSketch() as s1:
            Rectangle(w, h)
            fillet(s1.vertices(), radius=r)
        extrude(amount=d)

        # 2. Internal Cavity
        with BuildSketch(Plane.XY.offset(floor_t)) as s2:
            Rectangle(w - 2 * wall, h - 2 * wall)
            fillet(s2.vertices(), radius=max(0.5, r - wall))
        extrude(amount=d - floor_t + 1.0, mode=Mode.SUBTRACT)

        # 3. Rear Cylindrical Concave Pole Saddle (100mm radius arch)
        with BuildSketch(Plane.YZ) as s_saddle:
            with Locations((0, -2.0)):
                Circle(50.0)
        extrude(amount=w + 2.0, both=True, mode=Mode.SUBTRACT)

        # 4. Dual 15mm Jubilee Hose Clamp Channels across the rear (Height 16mm, Depth 3.5mm)
        with Locations((0, 34.0, 0), (0, -34.0, 0)):
            Box(w + 4.0, 16.0, 3.5, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        # 5. 6x Perimeter Fastener Bosses for M3 Brass Heat-Set Inserts
        boss_r = 4.4
        screw_positions = [
            (-w/2 + 8.5, -h/2 + 9.5),
            ( w/2 - 8.5, -h/2 + 9.5),
            ( w/2 - 8.5,  0.0),
            (-w/2 + 8.5,  0.0),
            ( w/2 - 8.5,  h/2 - 9.5),
            (-w/2 + 8.5,  h/2 - 9.5),
        ]
        with Locations([(x, y, floor_t) for x, y in screw_positions]):
            Cylinder(radius=boss_r, height=d - floor_t, align=(Align.CENTER, Align.CENTER, Align.MIN))

        # M3 Insert Pilot Holes (dia 4.2mm, depth 7.0mm)
        with Locations([(x, y, d) for x, y in screw_positions]):
            Hole(radius=2.1, depth=7.0)

        # 6. Upper Bay: Raspberry Pi Zero 2 W Floor Standoffs (58mm x 23mm)
        pi_center_y = 16.0
        pi_standoff_h = 5.0
        pi_offsets = [
            (-29.0, pi_center_y - 11.5),
            ( 29.0, pi_center_y - 11.5),
            ( 29.0, pi_center_y + 11.5),
            (-29.0, pi_center_y + 11.5),
        ]
        with Locations([(x, y, floor_t) for x, y in pi_offsets]):
            Cylinder(radius=2.8, height=pi_standoff_h, align=(Align.CENTER, Align.CENTER, Align.MIN))
            Hole(radius=1.3, depth=pi_standoff_h + 1.0)

        # 7. Lower Bay: 12V-to-5V Buck Regulator Standoffs (40mm x 20mm)
        buck_center_y = -36.0
        buck_offsets = [
            (-20.0, buck_center_y - 10.0),
            ( 20.0, buck_center_y - 10.0),
            ( 20.0, buck_center_y + 10.0),
            (-20.0, buck_center_y + 10.0),
        ]
        with Locations([(x, y, floor_t) for x, y in buck_offsets]):
            Cylinder(radius=2.6, height=5.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
            Hole(radius=1.2, depth=5.0)

        # 8. MPU-6500 Anti-Tamper Mounting Platform
        with Locations((w/2 - 16.0, 16.0, floor_t)):
            Box(12.0, 18.0, 3.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
            with Locations((0, -5.0, 3.0), (0, 5.0, 3.0)):
                Hole(radius=1.1, depth=3.0)

        # 9. Weatherproof Ingress Ports
        # Bottom Face: 2x PG7 Glands (dia 12.5mm) for Solar Panel & 12V Battery
        with BuildSketch(Plane.XZ.offset(-h/2)):
            with Locations((-20.0, floor_t + 11.0), (20.0, floor_t + 11.0)):
                Circle(radius=6.25)
        extrude(amount=wall + 3.0, mode=Mode.SUBTRACT)

        # Top Face: SMA Antenna Port (dia 6.5mm) for 4G LTE
        with BuildSketch(Plane.XZ.offset(h/2)):
            with Locations((24.0, floor_t + 11.0)):
                Circle(radius=3.25)
        extrude(amount=-(wall + 3.0), mode=Mode.SUBTRACT)

        # 10. Continuous Perimeter Gasket Groove on Top Lip
        with BuildSketch(Plane.XY.offset(d)):
            Rectangle(w - wall, h - wall)
            Rectangle(w - wall - 2.8, h - wall - 2.8, mode=Mode.SUBTRACT)
        extrude(amount=-1.8, mode=Mode.SUBTRACT)

    return base.part


def build_tier2_front_bezel():
    # Front Bezel Dimensions (mm)
    w, h, plate_t = 92.0, 116.0, 3.5
    r = 24.0
    cam_y = 38.0

    with BuildPart() as bezel:
        # 1. Smooth Stadium Front Faceplate
        with BuildSketch() as s:
            Rectangle(w, h)
            fillet(s.vertices(), radius=r)
        extrude(amount=plate_t)

        # 2. Camera Lens Aperture (dia 20.4mm)
        with Locations((0, cam_y, 0)):
            Hole(radius=10.2, depth=plate_t + 2.0)

        # 3. Semicircular Bulging Umbrella / Eyebrow Canopy (R=18mm Smooth Arch, 22mm Overhang)
        with BuildSketch(Plane.XZ.offset(cam_y + 2.0)) as s_visor:
            with Locations((0, plate_t)):
                with BuildLine():
                    Line((-18.0, 0), (18.0, 0))
                    RadiusArc((18.0, 0), (-18.0, 0), radius=18.0)
                make_face()
        extrude(amount=22.0)

        # Hollow optical cavity inside umbrella hood
        with BuildSketch(Plane.XZ.offset(cam_y + 2.0)) as s_cut:
            with Locations((0, plate_t)):
                with BuildLine():
                    Line((-15.4, 0), (15.4, 0))
                    RadiusArc((15.4, 0), (-15.4, 0), radius=15.4)
                make_face()
        extrude(amount=22.0 - 2.6, mode=Mode.SUBTRACT)

        # 4. Integrated 15° Angled Camera Mount Standoffs on the Inside (z < 0)
        cam_offsets = [
            (-10.5, cam_y - 6.25),
            ( 10.5, cam_y - 6.25),
            ( 10.5, cam_y + 6.25),
            (-10.5, cam_y + 6.25),
        ]
        for x, y in cam_offsets:
            with Locations((x, y, 0)):
                Cylinder(radius=2.4, height=5.0, align=(Align.CENTER, Align.CENTER, Align.MAX))
                Hole(radius=1.0, depth=5.0)

        # 5. 6x Recessed Countersunk Hex Screw Pockets
        screw_positions = [
            (-w/2 + 8.5, -h/2 + 9.5),
            ( w/2 - 8.5, -h/2 + 9.5),
            ( w/2 - 8.5,  0.0),
            (-w/2 + 8.5,  0.0),
            ( w/2 - 8.5,  h/2 - 9.5),
            (-w/2 + 8.5,  h/2 - 9.5),
        ]
        with Locations([(x, y, 0) for x, y in screw_positions]):
            Hole(radius=1.7, depth=plate_t + 2.0)
            with Locations((0, 0, plate_t - 1.5)):
                Cylinder(radius=3.4, height=2.0, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        # 6. Continuous Perimeter Sealing Tongue
        with BuildSketch(Plane.XY):
            Rectangle(w - 2.6 - 0.4, h - 2.6 - 0.4)
            Rectangle(w - 2.6 - 2.4, h - 2.6 - 2.4, mode=Mode.SUBTRACT)
        extrude(amount=-1.5)

    return bezel.part


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out_dir, exist_ok=True)

    print("🛡️ Compiling Desert-Grade Bullet Pod Shell 2 (Package B: Solar Sentry)...")
    base = build_tier2_base_casing()
    bezel = build_tier2_front_bezel()

    export_step(base, os.path.join(out_dir, "shell_tier2_base_casing.step"))
    export_stl(base, os.path.join(out_dir, "shell_tier2_base_casing.stl"))
    export_step(bezel, os.path.join(out_dir, "shell_tier2_front_bezel.step"))
    export_stl(bezel, os.path.join(out_dir, "shell_tier2_front_bezel.stl"))

    # Complete 2-Piece Assembly
    assembly = Compound([
        base,
        bezel.moved(Location((0, 0, 32.0)))
    ])
    export_step(assembly, os.path.join(out_dir, "shell_tier2_complete_assembly.step"))
    print("  ✅ Shell 2 (Bullet Pod with Semicircular Umbrella Visor) Compiled Successfully!")
