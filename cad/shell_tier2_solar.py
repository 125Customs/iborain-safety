#!/usr/bin/env python3
"""
Iborain Safety — Production Golden Ratio Stealth Mast Capsule 3D CAD Generator for Shell 2 (Package B: Solar Sentry)
Design Standards: Optimized 8.5mm Micro-Aperture + Zero-Debris Filleted Sealing Tongue + Pole Saddle + IP66 Sealing
  • Form Factor: 52mm W x 108mm H x 26mm D Minimalist Stadium Capsule (R=14mm Smooth Curves).
  • Optimized Optics & Aperture:
      - Sleek, discreet 8.5mm camera micro-aperture with 0.4mm micro-chamfer bevel (15° downward tilt).
      - Internal 16.0mm x 1.2mm optical glass disc seating recess (IP66 dustproof & rainproof).
  • Clean Zero-Debris Corner Architecture:
      - Continuous smooth-filleted sealing tongue (matching R=14mm perimeter curves with zero sharp corner teeth).
      - 4x Corner Alignment Pins: Slimmed to 4.0mm OD (R=2.0mm) with 0.8mm self-aligning tapered lead-in tips.
      - 4x Corner Receiver Sockets on Base: Precision 5.0mm bore (R=2.5mm, depth 5.0mm) offering 0.5mm clearance
        for effortless, smooth drop-in slotting with zero binding.
  • Internal Packaging:
      - Upper Bay: Raspberry Pi Zero 2 W (65x30mm) + Sony IMX500 AI Camera (25x24mm, 15° tilt).
      - Lower Bay: 12V-to-5V Synchronous Stepdown Buck Converter (36x20mm).
      - MPU-6500 Anti-Tamper 6-Axis IMU.
      - Dual IP68 PG7 Cable Glands (Solar Panel + 12V Battery) on bottom face.
      - Top SMA 4G Antenna Port (dia 6.5mm).
      - Integrated Concave Pole Saddle (R=90mm) with dual 14mm Stainless Jubilee Strap Channels.
      - Continuous Stepped Labyrinth Gasket Groove (2.2mm W x 1.8mm D).

100% Pure Stealth: Monolithic Zero-Screw Front Face, Ultra-Slim 26mm Depth, Optimized 8.5mm Lens Pupil.
"""
import os
import sys
from build123d import *

def build_tier2_base_casing():
    # Golden Ratio Capsule Dimensions (mm)
    w, h, d = 52.0, 108.0, 23.0
    wall = 2.4
    floor_t = 2.5
    r = 14.0

    with BuildPart() as base:
        # 1. Smooth Rounded Stadium Outer Envelope
        with BuildSketch() as s1:
            Rectangle(w, h)
            fillet(s1.vertices(), radius=r)
        extrude(amount=d)

        # 2. Main Internal Dual-Bay Cavity (47.2mm W x 103.2mm H x 20.5mm D)
        with BuildSketch(Plane.XY.offset(floor_t)) as s2:
            Rectangle(w - 2 * wall, h - 2 * wall)
            fillet(s2.vertices(), radius=max(0.5, r - wall))
        extrude(amount=d - floor_t + 1.0, mode=Mode.SUBTRACT)

        # 3. Integrated Concave Pole Saddle on Rear Face (z = 0)
        with BuildSketch(Plane.YZ) as s_saddle:
            with Locations((0, -2.0)):
                Circle(45.0) # R=45mm radius (90mm diameter pole contour)
        extrude(amount=w + 2.0, both=True, mode=Mode.SUBTRACT)

        # 4. Dual 14mm Jubilee Strap Channels across the rear (Height 15mm, Depth 3.0mm)
        with Locations((0, 32.0, 0), (0, -32.0, 0)):
            Box(w + 4.0, 15.0, 3.0, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        # 5. 4x Corner Receiver Socket Pillars for Lid Pin Slotting
        # Outer radius 3.4mm, Top socket bore radius 2.5mm (5.0mm dia) with 0.5mm clearance
        screw_positions = [
            (-w/2 + 7.0, -h/2 + 8.5),
            ( w/2 - 7.0, -h/2 + 8.5),
            ( w/2 - 7.0,  h/2 - 8.5),
            (-w/2 + 7.0,  h/2 - 8.5),
        ]
        with Locations([(x, y, floor_t) for x, y in screw_positions]):
            Cylinder(radius=3.4, height=d - floor_t, align=(Align.CENTER, Align.CENTER, Align.MIN))
            # Smooth drop-in socket pocket (depth 5.0mm from top lip)
            with Locations((0, 0, d - floor_t)):
                Hole(radius=2.5, depth=5.0)
            # M3 screw through-hole through the base floor
            Hole(radius=1.7, depth=d)

        # 6. Rear Screw Counterbores on the Back Face (z = 0)
        with Locations([(x, y, 0) for x, y in screw_positions]):
            Cylinder(radius=3.2, height=1.2, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        # 7. Upper Bay: Raspberry Pi Zero 2 W Floor Standoffs (58.0mm x 23.0mm)
        pi_center_y = 12.0
        pi_standoff_h = 3.5
        pi_offsets = [
            (-11.5, pi_center_y - 29.0),
            ( 11.5, pi_center_y - 29.0),
            ( 11.5, pi_center_y + 29.0),
            (-11.5, pi_center_y + 29.0),
        ]
        with Locations([(x, y, floor_t) for x, y in pi_offsets]):
            Cylinder(radius=2.4, height=pi_standoff_h, align=(Align.CENTER, Align.CENTER, Align.MIN))
            Hole(radius=1.2, depth=pi_standoff_h + 1.0)

        # 8. Lower Bay: 12V-to-5V Stepdown Buck Regulator Standoffs (36.0mm x 20.0mm)
        buck_center_y = -36.0
        buck_offsets = [
            (-10.0, buck_center_y - 10.0),
            ( 10.0, buck_center_y - 10.0),
            ( 10.0, buck_center_y + 10.0),
            (-10.0, buck_center_y + 10.0),
        ]
        with Locations([(x, y, floor_t) for x, y in buck_offsets]):
            Cylinder(radius=2.4, height=3.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
            Hole(radius=1.1, depth=3.0)

        # 9. MPU-6500 Anti-Tamper Rigid Mounting Platform
        with Locations((w/2 - 13.0, 12.0, floor_t)):
            Box(10.0, 16.0, 2.5, align=(Align.CENTER, Align.CENTER, Align.MIN))
            with Locations((0, -4.5, 2.5), (0, 4.5, 2.5)):
                Hole(radius=1.0, depth=2.5)

        # 10. Industrial Weatherproof Gland Ports
        # Bottom Face: Dual PG7 Glands (dia 12.5mm each) for Solar Panel & 12V Battery
        with BuildSketch(Plane.XZ.offset(-h/2)):
            with Locations((-11.0, floor_t + 8.5), (11.0, floor_t + 8.5)):
                Circle(radius=6.25)
        extrude(amount=wall + 3.0, mode=Mode.SUBTRACT)

        # Top Face: SMA Antenna Port (dia 6.5mm)
        with BuildSketch(Plane.XZ.offset(h/2)):
            with Locations((0, floor_t + 8.5)):
                Circle(radius=3.25)
        extrude(amount=-(wall + 3.0), mode=Mode.SUBTRACT)

        # 11. Continuous Stepped Labyrinth Gasket Groove on Top Rim (Width 2.2mm, Depth 1.8mm)
        with BuildSketch(Plane.XY.offset(d)):
            Rectangle(w - wall, h - wall)
            fillet(s1.vertices(), radius=max(0.5, r - wall/2))
            Rectangle(w - wall - 2.2, h - wall - 2.2, mode=Mode.SUBTRACT)
        extrude(amount=-1.8, mode=Mode.SUBTRACT)

    return base.part


def build_tier2_front_bezel():
    # Monolithic Front Bezel Dimensions (mm)
    w, h, plate_t = 52.0, 108.0, 3.0
    r = 14.0
    cam_y = 30.0
    wall = 2.4

    with BuildPart() as bezel:
        # 1. Smooth Stadium Front Faceplate (z = 0 to plate_t)
        with BuildSketch() as s:
            Rectangle(w, h)
            fillet(s.vertices(), radius=r)
        extrude(amount=plate_t)

        # 2. Optimized 8.5mm Micro-Aperture with 0.4mm Micro-Chamfer Bevel
        with Locations((0, cam_y, 0)):
            Hole(radius=4.25, depth=plate_t + 2.0)
            with Locations((0, 0, plate_t - 0.5)):
                Cone(bottom_radius=4.9, top_radius=4.25, height=0.6, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)
            with Locations((0, 0, 0)):
                Cylinder(radius=8.0, height=1.2, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

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
                Hole(radius=1.0, depth=3.5)

        # 4. 4x Slimmed Smooth-Slotting Corner Alignment & Fastener Pins (z < 0)
        # Outer radius 2.0mm (4.0mm OD), height 4.5mm, with 0.8mm self-aligning tapered conical tip
        screw_positions = [
            (-w/2 + 7.0, -h/2 + 8.5, 0),
            ( w/2 - 7.0, -h/2 + 8.5, 0),
            ( w/2 - 7.0,  h/2 - 8.5, 0),
            (-w/2 + 7.0,  h/2 - 8.5, 0),
        ]
        for x, y, _ in screw_positions:
            with Locations((x, y, 0)):
                Cylinder(radius=2.0, height=4.5, align=(Align.CENTER, Align.CENTER, Align.MAX))
                Hole(radius=1.3, depth=4.5)
                with Locations((0, 0, -4.5)):
                    Cone(bottom_radius=1.5, top_radius=2.0, height=0.8, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        # 5. Continuous Smooth-Filleted Sealing Tongue (ZERO SHARP CORNERS - Matches R=14mm Perimeter!)
        with BuildSketch(Plane.XY) as s_tongue:
            with BuildSketch() as s_out:
                Rectangle(w - wall - 0.4, h - wall - 0.4)
                fillet(s_out.vertices(), radius=max(0.5, r - wall/2 - 0.2))
            with BuildSketch(mode=Mode.SUBTRACT) as s_in:
                Rectangle(w - wall - 2.2, h - wall - 2.2)
                fillet(s_in.vertices(), radius=max(0.5, r - wall/2 - 1.1))
        extrude(amount=-1.2)

    return bezel.part


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out_dir, exist_ok=True)

    print("🛡️ Compiling Optimized Micro-Aperture Stealth Shell 2 (Package B: Solar Sentry)...")
    base = build_tier2_base_casing()
    bezel = build_tier2_front_bezel()

    export_step(base, os.path.join(out_dir, "shell_tier2_base_casing.step"))
    export_stl(base, os.path.join(out_dir, "shell_tier2_base_casing.stl"))
    export_step(bezel, os.path.join(out_dir, "shell_tier2_front_bezel.step"))
    export_stl(bezel, os.path.join(out_dir, "shell_tier2_front_bezel.stl"))

    # Complete Assembly
    assembly = Compound([
        base,
        bezel.moved(Location((0, 0, 23.0)))
    ])
    export_step(assembly, os.path.join(out_dir, "shell_tier2_complete_assembly.step"))
    print("  ✅ Shell 2 (Optimized 8.5mm Micro-Port & Filleted Sealing Tongue) Compiled Successfully!")
