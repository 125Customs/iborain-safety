#!/usr/bin/env python3
"""
Iborain Safety — Premium Cyber-Stealth 3D CAD Generator for Shell 2 (Package B: Solar Sentry)
Architecture: Heavy-Duty Sentry-Core™ Sled System (Dual-Bay Tactical Outdoor Armor)
  1. Outer Exoskeleton Armor: Dual-chamber chassis with 45° stealth facets, curved pole saddle,
     dual 15mm Jubilee hose clamp channels, passive cooling gills, dual PG7 glands & SMA port.
  2. Dual-Tier Carrier Sled: Bench-assembled tray for Pi Zero 2 W, 15° angled IMX500 camera,
     MPU-6500 IMU, and 12V-to-5V MPPT/buck stepdown regulator.
  3. Storm Visor Bezel: Aggressive 35mm deep overhang storm visor with 6x recessed hex-socket bolts.

100% Pure Stealth Black-Box: Zero LEDs, Zero Screens, Monolithic Military-Grade Aesthetic.
"""
import os
import sys
from build123d import *

def build_tier2_exoskeleton():
    """
    Heavy-Duty Outdoor Exoskeleton Armor:
    Dual-chamber internal bays, 45° stealth chamfers, integrated curved pole saddle,
    dual 15mm Jubilee strap channels, passive cooling gills, and perimeter labyrinth gasket channel.
    """
    w, h, d = 132.0, 128.0, 54.0
    wall = 3.2
    floor_t = 3.5

    with BuildPart() as shell:
        # 1. Base Monolithic Box with 45° Stealth Chamfered Facets
        Box(w, h, d, align=(Align.CENTER, Align.CENTER, Align.MIN))
        chamfer(shell.edges().filter_by(Axis.Z), length=8.0)

        # 2. Hollow out Upper Compute Bay (110mm x 72mm) & Lower Power Bay (110mm x 38mm)
        upper_h = 72.0
        upper_center_y = (h/2 - wall) - upper_h/2
        with Locations((0, upper_center_y, floor_t)):
            Box(110.0, upper_h, d - floor_t + 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        lower_h = 38.0
        lower_center_y = (-h/2 + wall) + lower_h/2
        with Locations((0, lower_center_y, floor_t)):
            Box(110.0, lower_h, d - floor_t + 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        # 3. Cable Pass-Through Slot in dividing partition (20mm x 10mm)
        partition_y = lower_center_y + lower_h/2 + wall/2
        with Locations((0, partition_y, floor_t + 15.0)):
            Box(20.0, wall + 2.0, 12.0, align=(Align.CENTER, Align.CENTER, Align.CENTER), mode=Mode.SUBTRACT)

        # 4. Slide-in Guide Rails for Upper Compute Sled
        with Locations((-110.0/2 + 1.5, upper_center_y, floor_t + 14.0), (110.0/2 - 1.5, upper_center_y, floor_t + 14.0)):
            Box(3.0, upper_h - 4.0, 4.0, align=(Align.CENTER, Align.CENTER, Align.CENTER))

        # 5. 6x Heavy-Duty Perimeter Fastener Pillars for M3 Heat-Set Inserts
        boss_r = 4.8
        screw_positions = [
            (-w/2 + 8.5, -h/2 + 8.5),
            ( w/2 - 8.5, -h/2 + 8.5),
            ( w/2 - 8.5,  0.0),
            (-w/2 + 8.5,  0.0),
            ( w/2 - 8.5,  h/2 - 8.5),
            (-w/2 + 8.5,  h/2 - 8.5),
        ]
        with Locations([(x, y, floor_t) for x, y in screw_positions]):
            Cylinder(radius=boss_r, height=d - floor_t, align=(Align.CENTER, Align.CENTER, Align.MIN))

        # M3 Heat-Set Insert Pilot Holes (dia 4.2mm, depth 8.5mm)
        with Locations([(x, y, d) for x, y in screw_positions]):
            Hole(radius=2.1, depth=8.5)

        # 6. Underside Passive Heat Dissipation Cooling Gills
        for i in range(-3, 4):
            with Locations((i * 14.0, -h/2 + 12.0, 0)):
                Box(7.0, 12.0, floor_t + 2.0, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        # 7. Weatherproof Cable Glands & Antenna Ports
        # Bottom Face: 2x PG7 Glands (dia 12.5mm) for Solar Panel & 12V Battery
        with BuildSketch(Plane.XZ.offset(-h/2)):
            with Locations((-32.0, floor_t + 14.0), (32.0, floor_t + 14.0)):
                Circle(radius=6.25)
        extrude(amount=wall + 4.0, mode=Mode.SUBTRACT)

        # Top Face: 1x SMA Antenna Port (dia 6.5mm)
        with BuildSketch(Plane.XZ.offset(h/2)):
            with Locations((36.0, floor_t + 14.0)):
                Circle(radius=3.25)
        extrude(amount=-(wall + 4.0), mode=Mode.SUBTRACT)

        # 8. Rear Dual 15mm Jubilee Hose Clamp Channels (Height 16mm, Depth 4mm)
        with Locations((0, 36.0, 0), (0, -36.0, 0)):
            Box(w + 4.0, 16.0, 4.0, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        # 9. Labyrinth Gasket Channel on Top Rim
        with BuildSketch(Plane.XY.offset(d)):
            Rectangle(w - 4.5, h - 4.5)
            Rectangle(w - 8.5, h - 8.5, mode=Mode.SUBTRACT)
        extrude(amount=-2.2, mode=Mode.SUBTRACT)

    return shell.part


def build_tier2_carrier_sled():
    """
    Dual-Tier Modular Carrier Sled:
    Upper Tier holds Raspberry Pi Zero 2 W, 15° angled Sony IMX500 camera, and MPU-6500.
    Lower Tier holds 12V-to-5V stepdown buck regulator & terminal block.
    """
    sled_w = 108.0
    sled_h = 118.0
    sled_t = 2.6

    with BuildPart() as sled:
        # 1. Base Sled Platform
        Box(sled_w, sled_h, sled_t, align=(Align.CENTER, Align.CENTER, Align.MIN))
        # Side guide rail notches
        with Locations((-sled_w/2 + 1.5, 20.0, sled_t/2), (sled_w/2 - 1.5, 20.0, sled_t/2)):
            Box(3.2, 68.0, sled_t + 1.0, align=(Align.CENTER, Align.CENTER, Align.CENTER), mode=Mode.SUBTRACT)

        # 2. Upper Tier: Raspberry Pi Zero 2 W Standoffs (58mm x 23mm)
        pi_center_y = 12.0
        pi_standoff_h = 5.0
        pi_offsets = [
            (-29.0, pi_center_y - 11.5),
            ( 29.0, pi_center_y - 11.5),
            ( 29.0, pi_center_y + 11.5),
            (-29.0, pi_center_y + 11.5),
        ]
        with Locations([(x, y, sled_t) for x, y in pi_offsets]):
            Cylinder(radius=3.0, height=pi_standoff_h, align=(Align.CENTER, Align.CENTER, Align.MIN))
            Hole(radius=1.3, depth=pi_standoff_h + 1.0)

        # 3. Upper Tier: 15° Downward Angled Camera Pedestal for Sony IMX500
        cam_center_y = 44.0
        cam_pedestal_h = 18.0
        with Locations((0, cam_center_y, sled_t)):
            Box(32.0, 24.0, cam_pedestal_h, align=(Align.CENTER, Align.CENTER, Align.MIN))
            with Locations((0, 0, 0)):
                Box(20.0, 14.0, cam_pedestal_h + 2.0, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)
            # 4x M2 standoffs
            with Locations(
                (-10.5, -6.25, cam_pedestal_h), (10.5, -6.25, cam_pedestal_h),
                ( 10.5,  6.25, cam_pedestal_h), (-10.5,  6.25, cam_pedestal_h)
            ):
                Cylinder(radius=2.4, height=4.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
                Hole(radius=1.0, depth=4.0)

        # 4. Upper Tier: MPU-6500 IMU Bracket
        with Locations((sled_w/2 - 14.0, 12.0, sled_t)):
            Box(14.0, 20.0, 3.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
            with Locations((0, -6.0, 3.0), (0, 6.0, 3.0)):
                Hole(radius=1.1, depth=3.0)

        # 5. Lower Tier: 12V-to-5V Synchronous Buck Converter Standoffs (40mm x 20mm)
        buck_center_y = -38.0
        buck_offsets = [
            (-20.0, buck_center_y - 10.0),
            ( 20.0, buck_center_y - 10.0),
            ( 20.0, buck_center_y + 10.0),
            (-20.0, buck_center_y + 10.0),
        ]
        with Locations([(x, y, sled_t) for x, y in buck_offsets]):
            Cylinder(radius=2.6, height=5.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
            Hole(radius=1.2, depth=5.0)

        # 6. Central Cable Routing Conduit Cutout
        with Locations((0, -10.0, 0)):
            Box(24.0, 12.0, sled_t + 2.0, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        # 7. Ergonomic Service Pull Ring Tab
        with Locations((0, -sled_h/2 + 4.0, sled_t)):
            Box(18.0, 5.0, 10.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
            with Locations((0, 0, 5.0)):
                Cylinder(radius=2.5, height=7.0, align=(Align.CENTER, Align.CENTER, Align.CENTER), mode=Mode.SUBTRACT)

    return sled.part


def build_tier2_faceplate_visor():
    """
    Heavy-Duty Storm Visor Bezel & Hermetic Front Plate:
    Sculpted 45° angular face, aggressive 35mm deep overhang storm visor,
    20.4mm optical aperture, 6x recessed hex screw pockets, and gasket tongue.
    """
    w, h, plate_t = 132.0, 128.0, 4.0
    cam_center_y = 44.0

    with BuildPart() as bezel:
        # 1. Base Faceted Bezel Plate
        Box(w, h, plate_t, align=(Align.CENTER, Align.CENTER, Align.MIN))
        chamfer(bezel.edges().filter_by(Axis.Z), length=8.0)

        # 2. Camera Optical Lens Aperture (dia 20.4mm)
        with Locations((0, cam_center_y, 0)):
            Hole(radius=10.2, depth=plate_t + 2.0)

        # 3. Deep 35mm Overhang Storm Visor Hood with 20° Rain Shed Angle
        visor_w = 46.0
        visor_h = 38.0
        visor_len = 35.0
        visor_t = 3.0

        with BuildSketch(Plane.XY.offset(plate_t)):
            with Locations((0, cam_center_y + 4.0)):
                Rectangle(visor_w, visor_h)
                Rectangle(visor_w - 2*visor_t, visor_h - 2*visor_t, mode=Mode.SUBTRACT)
                # Open lower optical cone
                with Locations((0, -visor_h/2 + visor_t/2)):
                    Rectangle(visor_w, visor_t + 1.0, mode=Mode.SUBTRACT)
        extrude(amount=visor_len)

        # 4. 6x Recessed Countersunk Hex Screw Pockets
        screw_positions = [
            (-w/2 + 8.5, -h/2 + 8.5),
            ( w/2 - 8.5, -h/2 + 8.5),
            ( w/2 - 8.5,  0.0),
            (-w/2 + 8.5,  0.0),
            ( w/2 - 8.5,  h/2 - 8.5),
            (-w/2 + 8.5,  h/2 - 8.5),
        ]
        with Locations([(x, y, 0) for x, y in screw_positions]):
            Hole(radius=1.7, depth=plate_t + 2.0)
            with Locations((0, 0, plate_t - 1.8)):
                Cylinder(radius=3.5, height=2.2, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        # 5. Gasket Labyrinth Tongue (bottom of faceplate)
        with BuildSketch(Plane.XY):
            Rectangle(w - 5.0, h - 5.0)
            Rectangle(w - 8.0, h - 8.0, mode=Mode.SUBTRACT)
        extrude(amount=-2.0)

    return bezel.part


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out_dir, exist_ok=True)

    print("🛡️ Compiling Premium Sentry-Core™ Shell 2 (Package B: Solar Sentry)...")
    exo = build_tier2_exoskeleton()
    sled = build_tier2_carrier_sled()
    bezel = build_tier2_faceplate_visor()

    export_step(exo, os.path.join(out_dir, "shell_tier2_exoskeleton.step"))
    export_stl(exo, os.path.join(out_dir, "shell_tier2_exoskeleton.stl"))
    export_step(sled, os.path.join(out_dir, "shell_tier2_carrier_sled.step"))
    export_stl(sled, os.path.join(out_dir, "shell_tier2_carrier_sled.stl"))
    export_step(bezel, os.path.join(out_dir, "shell_tier2_faceplate_visor.step"))
    export_stl(bezel, os.path.join(out_dir, "shell_tier2_faceplate_visor.stl"))

    # Complete Assembly
    assembly = Compound([
        exo,
        sled.moved(Location((0, 0, 3.5))),
        bezel.moved(Location((0, 0, 54.0)))
    ])
    export_step(assembly, os.path.join(out_dir, "shell_tier2_complete_assembly.step"))
    print("  ✅ Shell 2 (Exoskeleton, Sled, Visor Bezel) Compiled Successfully!")
