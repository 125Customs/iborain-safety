#!/usr/bin/env python3
"""
Iborain Safety — Production Golden Ratio Stealth Capsule 3D CAD Generator for Shell 1 (Package A: Grid Sentry)
Design Standards: Guaranteed Component Clearance + Smooth-Slotting Corner Pins + IP66 Weatherproofing
  • Form Factor: 48mm W x 84mm H x 22mm D Minimalist Stealth Capsule (R=12mm Smooth Curves).
  • Refined Corner Pin Architecture:
      - 4x Corner Alignment / Fastener Pins on Lid: Slimmed to 4.8mm OD (R=2.4mm) with 0.8mm tapered lead-in tips.
      - 4x Corner Receiver Sockets on Base: Precision 5.4mm bore (R=2.7mm, depth 5.0mm) offering 0.3mm radial clearance
        for effortless, smooth drop-in slotting with zero binding.
      - Rear-entry M3 screw holes (3.4mm dia) passing through the base floor into the lid pins.
  • Internal Packaging:
      - Raspberry Pi Zero 2 W (65x30mm) on 3.5mm floor standoffs.
      - Sony IMX500 AI Camera (25x24mm) on front bezel interior with 45° beveled recessed optical eye.
      - MPU-6500 Anti-Tamper 6-Axis IMU.
      - Bottom IP68 PG7 Cable Gland (dia 12.5mm) & Top SMA 4G Antenna Port (dia 6.5mm).
      - Recessed 20.0mm x 1.2mm optical glass sealing disc seat.
      - Continuous Stepped Labyrinth Gasket Groove (2.0mm W x 1.6mm D).

100% Pure Stealth: Monolithic Zero-Screw Front Face, Ultra-Slim 22mm Depth, Smooth Drop-In Pin Slotting.
"""
import os
import sys
from build123d import *

def build_tier1_base_casing():
    # Golden Ratio Capsule Dimensions (mm)
    w, h, d = 48.0, 84.0, 19.5
    wall = 2.2
    floor_t = 2.2
    r = 12.0

    with BuildPart() as base:
        # 1. Smooth Double-Curved Outer Envelope (z = 0 to d)
        with BuildSketch() as s1:
            Rectangle(w, h)
            fillet(s1.vertices(), radius=r)
        extrude(amount=d)

        # 2. Main Internal Compute Cavity (43.6mm W x 79.6mm H x 17.3mm D)
        with BuildSketch(Plane.XY.offset(floor_t)) as s2:
            Rectangle(w - 2 * wall, h - 2 * wall)
            fillet(s2.vertices(), radius=max(0.5, r - wall))
        extrude(amount=d - floor_t + 1.0, mode=Mode.SUBTRACT)

        # 3. 4x Corner Receiver Socket Pillars for Lid Pin Slotting
        # Outer radius 3.5mm, Top socket bore radius 2.7mm (5.4mm dia) with 0.3mm radial clearance
        screw_positions = [
            (-w/2 + 6.5, -h/2 + 7.5),
            ( w/2 - 6.5, -h/2 + 7.5),
            ( w/2 - 6.5,  h/2 - 7.5),
            (-w/2 + 6.5,  h/2 - 7.5),
        ]
        with Locations([(x, y, floor_t) for x, y in screw_positions]):
            Cylinder(radius=3.5, height=d - floor_t, align=(Align.CENTER, Align.CENTER, Align.MIN))
            # Smooth drop-in socket pocket (depth 5.0mm from top lip)
            with Locations((0, 0, d - floor_t)):
                Hole(radius=2.7, depth=5.0)
            # M3 screw through-hole through the base floor
            Hole(radius=1.7, depth=d)

        # 4. Rear Screw Counterbores on the Back Face (z = 0)
        with Locations([(x, y, 0) for x, y in screw_positions]):
            Cylinder(radius=3.2, height=1.2, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        # 5. Standard Raspberry Pi Zero 2 W Floor Standoffs (58.0mm x 23.0mm)
        pi_center_y = -2.0
        pi_standoff_h = 3.5
        pi_offsets = [
            (-11.5, pi_center_y - 29.0),
            ( 11.5, pi_center_y - 29.0),
            ( 11.5, pi_center_y + 29.0),
            (-11.5, pi_center_y + 29.0),
        ]
        with Locations([(x, y, floor_t) for x, y in pi_offsets]):
            Cylinder(radius=2.4, height=pi_standoff_h, align=(Align.CENTER, Align.CENTER, Align.MIN))
            Hole(radius=1.2, depth=pi_standoff_h + 1.0) # M2.5 screw pilot

        # 6. MPU-6500 Anti-Tamper IMU Mounting Platform
        with Locations((w/2 - 12.0, 0, floor_t)):
            Box(10.0, 16.0, 2.5, align=(Align.CENTER, Align.CENTER, Align.MIN))
            with Locations((0, -4.5, 2.5), (0, 4.5, 2.5)):
                Hole(radius=1.0, depth=2.5)

        # 7. Industrial Weatherproof Ports
        # Bottom Face: PG7 IP68 Cable Gland (dia 12.5mm) for 5V DC Power
        with BuildSketch(Plane.XZ.offset(-h/2)):
            with Locations((0, floor_t + 7.5)):
                Circle(radius=6.25)
        extrude(amount=wall + 3.0, mode=Mode.SUBTRACT)

        # Top Face: SMA Female Bulkhead Port (dia 6.5mm) for 4G LTE Antenna
        with BuildSketch(Plane.XZ.offset(h/2)):
            with Locations((0, floor_t + 7.5)):
                Circle(radius=3.25)
        extrude(amount=-(wall + 3.0), mode=Mode.SUBTRACT)

        # 8. Rear Wall Mounting Pattern (4x M4 clearance holes, 32mm x 48mm grid)
        with Locations([(-16.0, -24.0, 0), (16.0, -24.0, 0), (16.0, 24.0, 0), (-16.0, 24.0, 0)]):
            Hole(radius=2.2, depth=floor_t + 2.0)

        # 9. Continuous Stepped Labyrinth Gasket Groove on Top Rim (Width 2.0mm, Depth 1.6mm)
        with BuildSketch(Plane.XY.offset(d)):
            Rectangle(w - wall, h - wall)
            fillet(s1.vertices(), radius=max(0.5, r - wall/2))
            Rectangle(w - wall - 2.0, h - wall - 2.0, mode=Mode.SUBTRACT)
        extrude(amount=-1.6, mode=Mode.SUBTRACT)

    return base.part


def build_tier1_front_bezel():
    # Monolithic Front Bezel Dimensions (mm)
    w, h, plate_t = 48.0, 84.0, 2.5
    r = 12.0
    cam_y = 16.0

    with BuildPart() as bezel:
        # 1. Smooth Stadium Front Faceplate (z = 0 to plate_t)
        with BuildSketch() as s:
            Rectangle(w, h)
            fillet(s.vertices(), radius=r)
        extrude(amount=plate_t)

        # 2. Recessed 45° Beveled Optical Eye Aperture with Internal Glass Disc Seat
        with Locations((0, cam_y, 0)):
            Hole(radius=8.0, depth=plate_t + 2.0)
            # 45-degree chamfered lead-in for anti-glare shading
            with Locations((0, 0, plate_t - 1.0)):
                Cone(bottom_radius=10.0, top_radius=8.0, height=1.2, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)
            # Internal 20mm x 1.2mm circular recess seat for waterproof optical glass / O-ring disc
            with Locations((0, 0, 0)):
                Cylinder(radius=10.0, height=1.2, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

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
                Hole(radius=1.0, depth=4.0) # M2 screw pilot

        # 4. 4x Slimmed Smooth-Slotting Corner Alignment & Fastener Pins (z < 0)
        # Outer radius 2.4mm (4.8mm dia), height 4.5mm, with 0.8mm self-aligning tapered conical tip
        screw_positions = [
            (-w/2 + 6.5, -h/2 + 7.5, 0),
            ( w/2 - 6.5, -h/2 + 7.5, 0),
            ( w/2 - 6.5,  h/2 - 7.5, 0),
            (-w/2 + 6.5,  h/2 - 7.5, 0),
        ]
        for x, y, _ in screw_positions:
            with Locations((x, y, 0)):
                # Main pin body (4.8mm OD, 4.5mm height)
                Cylinder(radius=2.4, height=4.5, align=(Align.CENTER, Align.CENTER, Align.MAX))
                # Internal pilot hole (1.3mm radius for M2.5/M3 thread or insert)
                Hole(radius=1.3, depth=4.5)
                # Tapered lead-in cone at the pin tip for effortless, self-guiding drop-in entry
                with Locations((0, 0, -4.5)):
                    Cone(bottom_radius=1.8, top_radius=2.4, height=0.8, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        # 5. Continuous Perimeter Sealing Tongue (1.6mm W x 1.2mm H)
        with BuildSketch(Plane.XY):
            Rectangle(w - 2.2 - 0.4, h - 2.2 - 0.4)
            Rectangle(w - 2.2 - 2.0, h - 2.2 - 2.0, mode=Mode.SUBTRACT)
        extrude(amount=-1.2)

    return bezel.part


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out_dir, exist_ok=True)

    print("🛡️ Compiling Production Golden Ratio Stealth Capsule Shell 1 (Refined Corner Pins)...")
    base = build_tier1_base_casing()
    bezel = build_tier1_front_bezel()

    export_step(base, os.path.join(out_dir, "shell_tier1_base_casing.step"))
    export_stl(base, os.path.join(out_dir, "shell_tier1_base_casing.stl"))
    export_step(bezel, os.path.join(out_dir, "shell_tier1_front_bezel.step"))
    export_stl(bezel, os.path.join(out_dir, "shell_tier1_front_bezel.stl"))

    # Complete Assembly
    assembly = Compound([
        base,
        bezel.moved(Location((0, 0, 19.5)))
    ])
    export_step(assembly, os.path.join(out_dir, "shell_tier1_complete_assembly.step"))
    print("  ✅ Shell 1 (Refined Slimmed Corner Pins & Sockets) Compiled Successfully!")
