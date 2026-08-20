#!/usr/bin/env python3
"""
Iborain Safety — Ultra-Slim Discreet Capsule 3D CAD Generator for Shell 1 (Package A: Grid Sentry)
Design Language: Smooth Rounded Pebble / Discreet Minimalist Optical Capsule (Strict 2-Piece System)
  1. Base Casing: Smooth 14mm-radius rounded body with direct Pi Zero 2 W standoffs, IMU bracket,
     PG7 power gland port, SMA antenna port, and continuous perimeter gasket groove.
  2. Front Bezel & Dome Visor: Sleek rounded faceplate with direct Sony IMX500 camera mounting standoffs,
     20.4mm optical aperture, smooth organic aerodynamic eyebrow visor, and flush countersunk screws.

100% Pure Stealth: Ultra-Slim (27mm total depth), Smooth Organic Contours, Zero Loose Gaps.
"""
import os
import sys
from build123d import *

def build_tier1_base_casing():
    # Capsule Dimensions (mm)
    w, h, d = 76.0, 78.0, 24.0
    wall = 2.4
    floor_t = 2.4
    r = 14.0

    with BuildPart() as base:
        # 1. Smooth Rounded Outer Envelope
        with BuildSketch() as s1:
            Rectangle(w, h)
            fillet(s1.vertices(), radius=r)
        extrude(amount=d)

        # 2. Internal Cavity (Leaving 2.4mm smooth walls and floor)
        with BuildSketch(Plane.XY.offset(floor_t)) as s2:
            Rectangle(w - 2 * wall, h - 2 * wall)
            fillet(s2.vertices(), radius=max(0.5, r - wall))
        extrude(amount=d - floor_t + 1.0, mode=Mode.SUBTRACT)

        # 3. 4x Corner Fastener Bosses for M3 Brass Heat-Set Inserts
        boss_r = 4.2
        corner_offsets = [
            (-w/2 + 6.5, -h/2 + 6.5),
            ( w/2 - 6.5, -h/2 + 6.5),
            ( w/2 - 6.5,  h/2 - 6.5),
            (-w/2 + 6.5,  h/2 - 6.5),
        ]
        with Locations([(x, y, floor_t) for x, y in corner_offsets]):
            Cylinder(radius=boss_r, height=d - floor_t, align=(Align.CENTER, Align.CENTER, Align.MIN))

        # M3 Insert Pilot Holes (dia 4.2mm, depth 6.5mm)
        with Locations([(x, y, d) for x, y in corner_offsets]):
            Hole(radius=2.1, depth=6.5)

        # 4. Raspberry Pi Zero 2 W Direct Floor Standoffs (58mm x 23mm)
        pi_center_y = -12.0
        pi_standoff_h = 5.0
        pi_offsets = [
            (-29.0, pi_center_y - 11.5),
            ( 29.0, pi_center_y - 11.5),
            ( 29.0, pi_center_y + 11.5),
            (-29.0, pi_center_y + 11.5),
        ]
        with Locations([(x, y, floor_t) for x, y in pi_offsets]):
            Cylinder(radius=2.8, height=pi_standoff_h, align=(Align.CENTER, Align.CENTER, Align.MIN))
            Hole(radius=1.3, depth=pi_standoff_h + 1.0) # M2.5 pilot

        # 5. MPU-6500 Anti-Tamper Mounting Pad
        with Locations((w/2 - 14.0, 0, floor_t)):
            Box(12.0, 18.0, 3.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
            with Locations((0, -5.0, 3.0), (0, 5.0, 3.0)):
                Hole(radius=1.1, depth=3.0)

        # 6. Weatherproof Ports
        # Bottom Face: PG7 IP68 Cable Gland (dia 12.5mm) for 5V DC power
        with BuildSketch(Plane.XZ.offset(-h/2)):
            with Locations((0, floor_t + 9.0)):
                Circle(radius=6.25)
        extrude(amount=wall + 3.0, mode=Mode.SUBTRACT)

        # Top Face: SMA Antenna Port (dia 6.5mm) for 4G LTE
        with BuildSketch(Plane.XZ.offset(h/2)):
            with Locations((20.0, floor_t + 9.0)):
                Circle(radius=3.25)
        extrude(amount=-(wall + 3.0), mode=Mode.SUBTRACT)

        # 7. Rear Wall Mounting Holes (4x M4 clearance holes, 48mm x 48mm grid)
        with Locations([(-24.0, -24.0, 0), (24.0, -24.0, 0), (24.0, 24.0, 0), (-24.0, 24.0, 0)]):
            Hole(radius=2.2, depth=floor_t + 2.0)

        # 8. Continuous Perimeter Gasket Groove on Top Lip (Zero-Gap Mating)
        with BuildSketch(Plane.XY.offset(d)):
            Rectangle(w - wall, h - wall)
            fillet(s1.vertices(), radius=max(0.5, r - wall/2))
            Rectangle(w - wall - 2.8, h - wall - 2.8, mode=Mode.SUBTRACT)
        extrude(amount=-1.8, mode=Mode.SUBTRACT)

    return base.part


def build_tier1_front_bezel():
    # Front Bezel Dimensions (mm)
    w, h, plate_t = 76.0, 78.0, 3.0
    r = 14.0
    cam_y = 18.0

    with BuildPart() as bezel:
        # 1. Smooth Rounded Front Faceplate
        with BuildSketch() as s:
            Rectangle(w, h)
            fillet(s.vertices(), radius=r)
        extrude(amount=plate_t)

        # 2. Camera Optical Lens Aperture (dia 20.4mm)
        with Locations((0, cam_y, 0)):
            Hole(radius=10.2, depth=plate_t + 2.0)

        # 3. Smooth Organic Aerodynamic Eyebrow Visor (18mm Overhang)
        visor_w = 34.0
        visor_h = 26.0
        visor_len = 18.0
        visor_t = 2.4

        with BuildSketch(Plane.XY.offset(plate_t)) as s_visor:
            with Locations((0, cam_y + 3.0)):
                Rectangle(visor_w, visor_h)
                fillet(s_visor.vertices(), radius=7.0)
                # Hollow optical cavity
                Rectangle(visor_w - 2*visor_t, visor_h - 2*visor_t, mode=Mode.SUBTRACT)
                # Open lower camera cone
                with Locations((0, -visor_h/2 + visor_t/2)):
                    Rectangle(visor_w + 2.0, visor_t + 1.0, mode=Mode.SUBTRACT)
        extrude(amount=visor_len)

        # 4. Sony IMX500 Direct Camera Mounting Standoffs on the Inside (z < 0)
        # Allows instant, zero-fuss camera mounting right behind the lens!
        cam_offsets = [
            (-10.5, cam_y - 6.25),
            ( 10.5, cam_y - 6.25),
            ( 10.5, cam_y + 6.25),
            (-10.5, cam_y + 6.25),
        ]
        for x, y in cam_offsets:
            with Locations((x, y, 0)):
                Cylinder(radius=2.2, height=4.5, align=(Align.CENTER, Align.CENTER, Align.MAX))
                Hole(radius=1.0, depth=4.5) # M2 screw pilot

        # 5. 4x Recessed Countersunk Hex Screw Pockets
        corner_offsets = [
            (-w/2 + 6.5, -h/2 + 6.5),
            ( w/2 - 6.5, -h/2 + 6.5),
            ( w/2 - 6.5,  h/2 - 6.5),
            (-w/2 + 6.5,  h/2 - 6.5),
        ]
        with Locations([(x, y, 0) for x, y in corner_offsets]):
            Hole(radius=1.7, depth=plate_t + 2.0)
            with Locations((0, 0, plate_t - 1.4)):
                Cylinder(radius=3.2, height=2.0, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        # 6. Continuous Perimeter Sealing Tongue (Mates flush into base groove)
        with BuildSketch(Plane.XY):
            Rectangle(w - 2.4 - 0.4, h - 2.4 - 0.4)
            Rectangle(w - 2.4 - 2.4, h - 2.4 - 2.4, mode=Mode.SUBTRACT)
        extrude(amount=-1.5)

    return bezel.part


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out_dir, exist_ok=True)

    print("🛡️ Compiling Smooth Ultra-Slim Shell 1 (Package A: Grid Sentry)...")
    base = build_tier1_base_casing()
    bezel = build_tier1_front_bezel()

    export_step(base, os.path.join(out_dir, "shell_tier1_base_casing.step"))
    export_stl(base, os.path.join(out_dir, "shell_tier1_base_casing.stl"))
    export_step(bezel, os.path.join(out_dir, "shell_tier1_front_bezel.step"))
    export_stl(bezel, os.path.join(out_dir, "shell_tier1_front_bezel.stl"))

    # Complete 2-Piece Assembly
    assembly = Compound([
        base,
        bezel.moved(Location((0, 0, 24.0)))
    ])
    export_step(assembly, os.path.join(out_dir, "shell_tier1_complete_assembly.step"))
    print("  ✅ Shell 1 (2-Piece Smooth Capsule) Compiled Successfully!")
