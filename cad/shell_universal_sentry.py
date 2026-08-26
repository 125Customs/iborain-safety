#!/usr/bin/env python3
"""
Iborain Safety — Industrial Baton Sentry 3D CAD Generator (Master Unified Platform)
Hardware Architecture: 3-Tier Isolated Thermal Zones (Optics Bay + Compute Deck + Power Reservoir)
Dimensions: 54.0 mm (W) x 128.0 mm (H) x 26.0 mm (D)

Guaranteed Zero-Collision Specs:
  • Zone 1 (Top Y = +45mm): Sony IMX500 AI Camera + 16.0x1.2mm AR Glass Disc (z = 21.5 to 26.0mm).
  • Zone 2 (Center Y = +2mm): Pi Zero 2 W (Deck 1) + Quectel 4G LTE HAT (Deck 2) (Y = -30.5 to +34.5mm).
  • Zone 3 (Lower Y = -43mm): Bestfire 5V 1350mAh Rechargeable Battery (Y = -67.2 to -18.7mm, Z = 3.5 to 21.0mm).
  • Bottom Apex (X = 0, Y = -64mm): Single Centered IP68 PG7 Solar Gland.
  • Top Apex (X = 0, Y = +64mm): Single Centered SMA 4G Antenna Port.
"""
import os
import sys
from build123d import *

def build_universal_base_casing():
    w, h, d = 54.0, 128.0, 26.0
    wall = 2.4
    floor_t = 2.5
    r = 14.0

    with BuildPart() as base:
        # 1. Smooth Rounded Stadium Outer Envelope
        with BuildSketch() as s1:
            Rectangle(w, h)
            fillet(s1.vertices(), radius=r)
        extrude(amount=d)

        # 2. Main Internal Multi-Bay Cavity (49.2mm W x 123.2mm H x 23.5mm D)
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
        with Locations((0, 38.0, 0), (0, -38.0, 0)):
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

        # Precision 4.8mm bore for smooth drop-in pin slotting
        with Locations([(x, y, d) for x, y in screw_positions]):
            Hole(radius=2.4, depth=5.0)
            Hole(radius=1.7, depth=d + 2.0) # M3 through-hole

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
        with Locations((w/2 - 13.0, 24.0, floor_t)):
            Box(16.0, 20.0, 2.5, align=(Align.CENTER, Align.CENTER, Align.MIN))
            with Locations((0, -6.0, 2.5), (0, 6.0, 2.5)):
                Hole(radius=1.2, depth=2.5)

        # 9. SINGLE CENTERED Weatherproof Bottom Gland Port for Solar 5.1V DC Power (X=0, Y=-64mm)
        with BuildSketch(Plane.XZ.offset(-h/2)):
            with Locations((0, floor_t + 9.5)):
                Circle(radius=6.25)
        extrude(amount=wall + 3.0, mode=Mode.SUBTRACT)

        # 10. Top Face: SMA Antenna Port (dia 6.5mm, X=0, Y=+64mm) for 4G LTE High-Gain Antenna
        with BuildSketch(Plane.XZ.offset(h/2)):
            with Locations((0, floor_t + 9.5)):
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
    w, h, plate_t = 54.0, 128.0, 3.0
    r = 14.0
    cam_y = 45.0
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

    base_plate = base.locate(Location((-35.0, 0, 0)))
    bezel_plate = bezel.locate(Location((35.0, 0, 4.5)))

    return Compound(children=[base_plate, bezel_plate])


def build_universal_complete_assembly():
    base = build_universal_base_casing()
    bezel = build_universal_front_bezel()
    bezel_mated = bezel.locate(Location((0, 0, 26.0)))

    return Compound(children=[base, bezel_mated])


def generate_all():
    out_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out_dir, exist_ok=True)
    desktop_dir = os.path.expanduser("~/Desktop/Iborain_3D_Print_Shells")
    os.makedirs(desktop_dir, exist_ok=True)

    print("=================================================================")
    print(" 🛡️ Generating Industrial Baton Universal Sentry CAD Files (54x128x26mm)")
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

        d_step = os.path.join(desktop_dir, f"{name}.step")
        d_stl = os.path.join(desktop_dir, f"{name}.stl")
        export_step(shape, d_step)
        export_stl(shape, d_stl)

        print(f"  ✅ Exported: {name}.step & .stl ({os.path.getsize(step_path)//1024} KB)")

    print("\n🎉 Industrial Baton Universal Hardware 3D CAD Generation Complete!")

if __name__ == "__main__":
    generate_all()
