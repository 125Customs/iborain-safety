#!/usr/bin/env python3
"""
Iborain Safety — Premium Cyber-Stealth 3D CAD Generator for Shell 1 (Package A: Grid Sentry)
Architecture: Modular Sentry-Core™ Sled System (3-Piece Assembly)
  1. Outer Exoskeleton Armor: Faceted stealth chassis with slide-in guide rails & labyrinth gasket channel.
  2. Internal Carrier Sled: Bench-assembled electronics tray for Pi Zero 2 W, Sony IMX500, and IMU.
  3. Faceted Visor Bezel: Aggressive 25mm hooded aerodynamic visor with recessed hex-socket fasteners.

100% Pure Stealth Black-Box: Zero LEDs, Zero Screens, Monolithic Dark-Tech Aesthetic.
"""
import os
import sys
from build123d import *

def build_tier1_exoskeleton():
    """
    Outer Exoskeleton Armor:
    Faceted angular chamfers (45°), internal slide-in guide rails,
    passive cooling gills on the underside, PG7 power gland port, and SMA antenna port.
    """
    w, h, d = 96.0, 92.0, 40.0
    wall = 2.8
    floor_t = 3.0

    with BuildPart() as shell:
        # 1. Base Monolithic Box with 45° Stealth Chamfered Facets
        Box(w, h, d, align=(Align.CENTER, Align.CENTER, Align.MIN))
        # Chamfer the 4 vertical corners for aggressive tactical stealth look
        chamfer(shell.edges().filter_by(Axis.Z), length=7.0)

        # 2. Main Internal Insertion Cavity
        cavity_w = 76.0
        cavity_h = 74.0
        cavity_d = d - floor_t + 1.0
        with Locations((0, 0, floor_t)):
            Box(cavity_w, cavity_h, cavity_d, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        # 3. Slide-in Guide Rails for the Internal Carrier Sled (Left & Right Walls)
        rail_w = 3.0
        rail_h = 4.0
        # Extrude guide rail ridges along the internal Z walls
        with Locations((-cavity_w/2 + rail_w/2, 0, floor_t + 12.0), (cavity_w/2 - rail_w/2, 0, floor_t + 12.0)):
            Box(rail_w, cavity_h - 4.0, rail_h, align=(Align.CENTER, Align.CENTER, Align.CENTER))

        # 4. Corner Fastener Pillars for M3 Brass Heat-Set Inserts
        boss_r = 4.5
        corner_offsets = [
            (-w/2 + 8.0, -h/2 + 8.0),
            ( w/2 - 8.0, -h/2 + 8.0),
            ( w/2 - 8.0,  h/2 - 8.0),
            (-w/2 + 8.0,  h/2 - 8.0),
        ]
        with Locations([(x, y, floor_t) for x, y in corner_offsets]):
            Cylinder(radius=boss_r, height=d - floor_t, align=(Align.CENTER, Align.CENTER, Align.MIN))

        # M3 Heat-Set Insert Pilot Holes (dia 4.2mm, depth 8.0mm)
        with Locations([(x, y, d) for x, y in corner_offsets]):
            Hole(radius=2.1, depth=8.0)

        # 5. Bottom Underside Passive Cooling Gills & Heat Dissipation Ribs
        # 4 angled tactical gill slots on the lower floor
        for i in range(-2, 3):
            with Locations((i * 12.0, -h/2 + 10.0, 0)):
                Box(6.0, 10.0, floor_t + 2.0, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        # 6. Weatherproof Ingress Ports
        # Bottom Face: PG7 IP68 Cable Gland (dia 12.5mm)
        with BuildSketch(Plane.XZ.offset(-h/2)):
            with Locations((0, floor_t + 12.0)):
                Circle(radius=6.25)
        extrude(amount=wall + 4.0, mode=Mode.SUBTRACT)

        # Top Face: SMA Female Bulkhead Port (dia 6.5mm)
        with BuildSketch(Plane.XZ.offset(h/2)):
            with Locations((26.0, floor_t + 12.0)):
                Circle(radius=3.25)
        extrude(amount=-(wall + 4.0), mode=Mode.SUBTRACT)

        # 7. Rear Wall Mounting Keyholes & M4 Fasteners (60mm x 60mm grid)
        with Locations([(-30.0, -30.0, 0), (30.0, -30.0, 0), (30.0, 30.0, 0), (-30.0, 30.0, 0)]):
            Hole(radius=2.2, depth=floor_t + 2.0)

        # 8. Precision Labyrinth Gasket Channel (Mating rim on top lip)
        with BuildSketch(Plane.XY.offset(d)):
            Rectangle(w - 4.0, h - 4.0)
            Rectangle(w - 7.5, h - 7.5, mode=Mode.SUBTRACT)
        extrude(amount=-2.2, mode=Mode.SUBTRACT)

    return shell.part


def build_tier1_carrier_sled():
    """
    Internal Modular Carrier Sled:
    Holds the Raspberry Pi Zero 2 W, Sony IMX500 Camera, and MPU-6500 IMU.
    Allows complete bench wiring and testing before sliding smoothly into the Exoskeleton.
    """
    sled_w = 75.0
    sled_h = 73.0
    sled_t = 2.4

    with BuildPart() as sled:
        # 1. Base Sled Platform
        Box(sled_w, sled_h, sled_t, align=(Align.CENTER, Align.CENTER, Align.MIN))
        # Side guide rail notches
        with Locations((-sled_w/2 + 1.5, 0, sled_t/2), (sled_w/2 - 1.5, 0, sled_t/2)):
            Box(3.2, sled_h + 2.0, sled_t + 1.0, align=(Align.CENTER, Align.CENTER, Align.CENTER), mode=Mode.SUBTRACT)

        # 2. Raspberry Pi Zero 2 W Mounting Standoffs (58mm x 23mm)
        pi_center_y = -14.0
        pi_standoff_h = 5.0
        pi_offsets = [
            (-29.0, pi_center_y - 11.5),
            ( 29.0, pi_center_y - 11.5),
            ( 29.0, pi_center_y + 11.5),
            (-29.0, pi_center_y + 11.5),
        ]
        with Locations([(x, y, sled_t) for x, y in pi_offsets]):
            Cylinder(radius=2.8, height=pi_standoff_h, align=(Align.CENTER, Align.CENTER, Align.MIN))
            Hole(radius=1.3, depth=pi_standoff_h + 1.0) # Self-tapping M2.5 / direct pilot

        # 3. Sony IMX500 Camera Elevated Optical Pedestal (21mm x 12.5mm)
        cam_center_y = 20.0
        cam_pedestal_h = 16.0
        with Locations((0, cam_center_y, sled_t)):
            Box(28.0, 20.0, cam_pedestal_h, align=(Align.CENTER, Align.CENTER, Align.MIN))
            # Optical through-window for camera rear components
            with Locations((0, 0, 0)):
                Box(18.0, 12.0, cam_pedestal_h + 2.0, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)
            # 4x M2 mounting corner standoffs
            with Locations(
                (-10.5, -6.25, cam_pedestal_h), (10.5, -6.25, cam_pedestal_h),
                ( 10.5,  6.25, cam_pedestal_h), (-10.5,  6.25, cam_pedestal_h)
            ):
                Cylinder(radius=2.4, height=4.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
                Hole(radius=1.0, depth=4.0)

        # 4. MPU-6500 Anti-Tamper Rigid Mounting Bracket
        with Locations((sled_w/2 - 12.0, -14.0, sled_t)):
            Box(14.0, 18.0, 3.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
            with Locations((0, -5.0, 3.0), (0, 5.0, 3.0)):
                Hole(radius=1.1, depth=3.0)

        # 5. Ergonomic Finger Pull Tab (for quick extraction / servicing)
        with Locations((0, -sled_h/2 + 4.0, sled_t)):
            Box(16.0, 5.0, 8.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
            with Locations((0, 0, 4.0)):
                Cylinder(radius=2.0, height=6.0, align=(Align.CENTER, Align.CENTER, Align.CENTER), mode=Mode.SUBTRACT)

    return sled.part


def build_tier1_faceplate_visor():
    """
    Faceted Visor Bezel & Hermetic Front Plate:
    Sculpted 45° angular face, aggressive 25mm overhang storm visor hood,
    20.4mm optical aperture, recessed hex screw pockets, and compressible silicone gasket tongue.
    """
    w, h, plate_t = 96.0, 92.0, 3.5
    cam_center_y = 20.0

    with BuildPart() as bezel:
        # 1. Base Faceted Bezel Plate
        Box(w, h, plate_t, align=(Align.CENTER, Align.CENTER, Align.MIN))
        chamfer(bezel.edges().filter_by(Axis.Z), length=7.0)

        # 2. Camera Optical Lens Aperture (dia 20.4mm)
        with Locations((0, cam_center_y, 0)):
            Hole(radius=10.2, depth=plate_t + 2.0)

        # 3. Aerodynamic Integrated Storm Visor Hood (25mm overhang with 20° downward rain slope)
        visor_w = 40.0
        visor_h = 32.0
        visor_len = 25.0
        visor_t = 2.6

        with BuildSketch(Plane.XY.offset(plate_t)):
            with Locations((0, cam_center_y + 4.0)):
                Rectangle(visor_w, visor_h)
                Rectangle(visor_w - 2*visor_t, visor_h - 2*visor_t, mode=Mode.SUBTRACT)
                # Open lower optical cone
                with Locations((0, -visor_h/2 + visor_t/2)):
                    Rectangle(visor_w, visor_t + 1.0, mode=Mode.SUBTRACT)
        extrude(amount=visor_len)

        # 4. 4x Recessed Countersunk Hex Screw Pockets
        corner_offsets = [
            (-w/2 + 8.0, -h/2 + 8.0),
            ( w/2 - 8.0, -h/2 + 8.0),
            ( w/2 - 8.0,  h/2 - 8.0),
            (-w/2 + 8.0,  h/2 - 8.0),
        ]
        with Locations([(x, y, 0) for x, y in corner_offsets]):
            Hole(radius=1.7, depth=plate_t + 2.0) # M3 clearance
            with Locations((0, 0, plate_t - 1.6)):
                Cylinder(radius=3.4, height=2.0, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        # 5. Gasket Labyrinth Tongue (bottom of faceplate)
        with BuildSketch(Plane.XY):
            Rectangle(w - 4.5, h - 4.5)
            Rectangle(w - 7.0, h - 7.0, mode=Mode.SUBTRACT)
        extrude(amount=-1.8)

    return bezel.part


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out_dir, exist_ok=True)

    print("🛡️ Compiling Premium Sentry-Core™ Shell 1 (Package A: Grid Sentry)...")
    exo = build_tier1_exoskeleton()
    sled = build_tier1_carrier_sled()
    bezel = build_tier1_faceplate_visor()

    export_step(exo, os.path.join(out_dir, "shell_tier1_exoskeleton.step"))
    export_stl(exo, os.path.join(out_dir, "shell_tier1_exoskeleton.stl"))
    export_step(sled, os.path.join(out_dir, "shell_tier1_carrier_sled.step"))
    export_stl(sled, os.path.join(out_dir, "shell_tier1_carrier_sled.stl"))
    export_step(bezel, os.path.join(out_dir, "shell_tier1_faceplate_visor.step"))
    export_stl(bezel, os.path.join(out_dir, "shell_tier1_faceplate_visor.stl"))

    # Complete Assembly
    assembly = Compound([
        exo,
        sled.moved(Location((0, 0, 3.0))),
        bezel.moved(Location((0, 0, 40.0)))
    ])
    export_step(assembly, os.path.join(out_dir, "shell_tier1_complete_assembly.step"))
    print("  ✅ Shell 1 (Exoskeleton, Sled, Visor Bezel) Compiled Successfully!")
