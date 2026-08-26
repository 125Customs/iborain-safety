#!/usr/bin/env python3
"""
Iborain Safety — The Unified Universal Autonomous Solar Sentry (Master 3D CAD Generator)
Hardware Architecture: Clean Tri-Zone Layout (Optics Bay + Center Compute Stack + Lower Dedicated Power Bay)
Dimensions: 52.0 mm (W) x 108.0 mm (H) x 24.0 mm (D)

Key Engineering Features:
  1. Zero Geometric Overlap / Zero Clumping:
     • Top Zone (Y = +34mm): Sony IMX500 AI Camera + 16mm AR Glass Disc.
     • Center Zone (Y = 0mm): Raspberry Pi Zero 2 W (Deck 1) + Quectel 4G LTE HAT (Deck 2).
     • Lower Zone (Y = -32mm): Bestfire 5V 1350mAh Rechargeable Battery in dedicated cradle.
  2. Single Centered Bottom PG7 Port (X = 0, Y = -54mm): 8.0mm wire curve clearance for solar DC power in.
  3. Single Top SMA Port (X = 0, Y = +54mm): Direct 18mm micro-coax run to modem U.FL port.
  4. Universal 2-in-1 Mounting: Rear concave pole saddle (R = 45mm) + 2x 14mm jubilee strap channels + M4 wall grid.
"""
import os
import sys
from build123d import *

def build_universal_base_casing():
    # Master Dimensions (mm)
    w, h, d = 52.0, 108.0, 24.0
    wall = 2.4
    floor_t = 2.5
    r = 14.0

    with BuildPart() as base:
        # 1. Smooth Rounded Stadium Outer Envelope
        with BuildSketch() as s1:
            Rectangle(w, h)
            fillet(s1.vertices(), radius=r)
        extrude(amount=d)

        # 2. Main Internal Multi-Bay Cavity (47.2mm W x 103.2mm H x 21.5mm D)
        with BuildSketch(Plane.XY.offset(floor_t)) as s2:
            Rectangle(w - 2 * wall, h - 2 * wall)
            fillet(s2.vertices(), radius=max(0.5, r - wall))
        extrude(amount=d - floor_t + 1.0, mode=Mode.SUBTRACT)

        # 3. Integrated Concave Pole Saddle on Rear Face (z = 0)
        with BuildSketch(Plane.YZ) as s_saddle:
            with Locations((0, -2.0)):
                Circle(45.0) # R=45mm radius (90mm diameter pole contour)
        extrude(amount=w + 2.0, both=True, mode=Mode.SUBTRACT)

        # 4. Dual 14mm Jubilee Strap Channels across the rear (Height 15.0mm, Depth 3.0mm)
        with Locations((0, 32.0, 0), (0, -32.0, 0)):
            Box(w + 4.0, 15.0, 3.0, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        # 5. 4x Corner Receiver Socket Pillars for Lid Pin Slotting
        screw_positions = [
            (-w/2 + 7.0, -h/2 + 8.5),
            ( w/2 - 7.0, -h/2 + 8.5),
            ( w/2 - 7.0,  h/2 - 8.5),
            (-w/2 + 7.0,  h/2 - 8.5),
        ]
        with Locations([(x, y, floor_t) for x, y in screw_positions]):
            Cylinder(radius=3.4, height=d - floor_t, align=(Align.CENTER, Align.CENTER, Align.MIN))

        # Precision 4.8mm bore (depth 5.0mm from top rim z=d) for smooth drop-in pin slotting
        with Locations([(x, y, d) for x, y in screw_positions]):
            Hole(radius=2.4, depth=5.0)
            # M3 screw through-hole through the base floor
            Hole(radius=1.7, depth=d + 2.0)

        # 6. Rear Screw Counterbores on the Back Face (z = 0)
        with Locations([(x, y, 0) for x, y in screw_positions]):
            Cylinder(radius=3.2, height=1.4, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        # 7. Center Compute Standoffs: Raspberry Pi Zero 2 W + 4G LTE HAT (58.0mm x 23.0mm, centered at Y = +2.0mm)
        compute_center_y = 2.0
        pi_standoff_h = 3.0
        pi_offsets = [
            (-11.5, compute_center_y - 29.0),
            ( 11.5, compute_center_y - 29.0),
            ( 11.5, compute_center_y + 29.0),
            (-11.5, compute_center_y + 29.0),
        ]
        with Locations([(x, y, floor_t) for x, y in pi_offsets]):
            Cylinder(radius=2.4, height=pi_standoff_h, align=(Align.CENTER, Align.CENTER, Align.MIN))
            Hole(radius=1.2, depth=pi_standoff_h + 1.0) # M2.5 screw pilot

        # 8. MPU-6500 / ICM-20948 Anti-Tamper Rigid Mounting Platform (16.0mm x 22.0mm x 2.5mm)
        with Locations((w/2 - 13.0, 18.0, floor_t)):
            Box(16.0, 20.0, 2.5, align=(Align.CENTER, Align.CENTER, Align.MIN))
            with Locations((0, -6.0, 2.5), (0, 6.0, 2.5)):
                Hole(radius=1.2, depth=2.5) # M2.5 IMU mounting holes

        # 9. SINGLE CENTERED Weatherproof Bottom Gland Port for Solar 5.1V DC Power (X=0, Y=-54mm)
        with BuildSketch(Plane.XZ.offset(-h/2)):
            with Locations((0, floor_t + 8.5)):
                Circle(radius=6.25)
        extrude(amount=wall + 3.0, mode=Mode.SUBTRACT)

        # 10. Top Face: SMA Antenna Port (dia 6.5mm, X=0, Y=+54mm) for 4G LTE High-Gain Antenna
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


def build_universal_front_bezel():
    # Monolithic Front Bezel Dimensions (mm)
    w, h, plate_t = 52.0, 108.0, 3.0
    r = 14.0
    cam_y = 34.0
    wall = 2.4

    with BuildPart() as bezel:
        # 1. Smooth Stadium Front Faceplate (z = 0 to plate_t)
        with BuildSketch() as s:
            Rectangle(w, h)
            fillet(s.vertices(), radius=r)
        extrude(amount=plate_t)

        # 2. Optimized 8.5mm Micro-Aperture with 0.4mm Micro-Chamfer Bevel & Internal Glass Recess
        with Locations((0, cam_y, 0)):
            # Precision 8.5mm optical through-hole
            Hole(radius=4.25, depth=plate_t + 2.0)
            # 0.4mm micro-chamfer lead-in on exterior face
            with Locations((0, 0, plate_t - 0.5)):
                Cone(bottom_radius=4.9, top_radius=4.25, height=0.6, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)
            # Internal 16.0mm x 1.2mm circular optical glass disc seating recess (IP66 sealing)
            with Locations((0, 0, 0)):
                Cylinder(radius=8.0, height=1.2, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        # 3. Direct Sony IMX500 Outward-Facing Camera Mounting Grid (21.0mm x 12.5mm, z < 0)
        cam_offsets = [
            (-10.5, cam_y - 6.25),
            ( 10.5, cam_y - 6.25),
            ( 10.5, cam_y + 6.25),
            (-10.5, cam_y + 6.25),
        ]
        for x, y in cam_offsets:
            with Locations((x, y, 0)):
                Cylinder(radius=2.0, height=3.5, align=(Align.CENTER, Align.CENTER, Align.MAX))
                Hole(radius=1.0, depth=3.5) # M2 screw pilot

        # 4. 4x Slimmed Smooth-Slotting Corner Alignment & Fastener Pins (z < 0)
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

        # 5. Continuous Smooth-Filleted Sealing Tongue (Matching R=14mm Perimeter with +0.3mm Clearance)
        with BuildSketch(Plane.XY) as s_tongue:
            with BuildSketch() as s_out:
                Rectangle(w - wall - 0.5, h - wall - 0.5)
                fillet(s_out.vertices(), radius=max(0.5, r - wall/2 - 0.25))
            with BuildSketch(mode=Mode.SUBTRACT) as s_in:
                Rectangle(w - wall - 2.2, h - wall - 2.2)
                fillet(s_in.vertices(), radius=max(0.5, r - wall/2 - 1.1))
        extrude(amount=-1.3)

    return bezel.part


def build_universal_side_by_side_plate():
    base = build_universal_base_casing()
    bezel = build_universal_front_bezel()

    # Position Base on Left (X = -35mm) with bottom face (z = 0) sitting flat on print bed
    base_plate = base.locate(Location((-35.0, 0, 0)))

    # Position Front Bezel on Right (X = +35mm) with internal bosses pointing DOWN and smooth front face pointing UP
    bezel_plate = bezel.locate(Location((35.0, 0, 4.5)))

    return Compound(children=[base_plate, bezel_plate])


def build_universal_complete_assembly():
    base = build_universal_base_casing()
    bezel = build_universal_front_bezel()

    # Mated location: Bezel seated flush at z = 24.0mm on top rim of base
    bezel_mated = bezel.locate(Location((0, 0, 24.0)))

    return Compound(children=[base, bezel_mated])


def generate_all():
    out_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out_dir, exist_ok=True)
    desktop_dir = os.path.expanduser("~/Desktop/Iborain_3D_Print_Shells")
    os.makedirs(desktop_dir, exist_ok=True)

    print("=================================================================")
    print(" 🛡️ Generating Clean Tri-Zone Universal Sentry CAD Files")
    print("=================================================================")

    base = build_universal_base_casing()
    bezel = build_universal_front_bezel()
    plate = build_universal_side_by_side_plate()
    assembly = build_universal_complete_assembly()

    models = {
        "shell_universal_base_casing": base,
        "shell_universal_front_bezel": bezel,
        "shell_universal_side_by_side_plate": plate,
        "shell_universal_complete_assembly": assembly,
        # Backward compatibility aliases
        "shell_tier2_base_casing": base,
        "shell_tier2_front_bezel": bezel,
        "shell_tier2_side_by_side_plate": plate,
        "shell_tier2_complete_assembly": assembly
    }

    for name, shape in models.items():
        step_path = os.path.join(out_dir, f"{name}.step")
        stl_path = os.path.join(out_dir, f"{name}.stl")
        
        export_step(shape, step_path)
        export_stl(shape, stl_path)

        # Mirror to Desktop
        d_step = os.path.join(desktop_dir, f"{name}.step")
        d_stl = os.path.join(desktop_dir, f"{name}.stl")
        export_step(shape, d_step)
        export_stl(shape, d_stl)

        print(f"  ✅ Exported: {name}.step & .stl ({os.path.getsize(step_path)//1024} KB)")

    print("\n🎉 Clean Tri-Zone Universal Hardware 3D CAD Generation Complete!")

if __name__ == "__main__":
    generate_all()
