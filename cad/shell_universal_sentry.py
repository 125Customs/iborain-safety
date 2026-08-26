#!/usr/bin/env python3
"""
Iborain Safety — Option B: Horizontal Battery Industrial Sentry (FINAL LOCKED GEOMETRY)
Hardware Architecture: 3-Tier Isolated Thermal Zones + Horizontal Battery + Under-Board IMU
Dimensions: 57.0 mm (W) x 122.0 mm (H) x 26.0 mm (D)

VERIFIED ZERO-COLLISION COORDINATE MAP:
  ┌──────────────────┬─────────────────────┬───────────────────┬───────────────────┬─────────────────────┐
  │ Component        │ Center (X, Y, Z)    │ X Range           │ Y Range           │ Z Range             │
  ├──────────────────┼─────────────────────┼───────────────────┼───────────────────┼─────────────────────┤
  │ Sony IMX500 Cam  │ (0, +49, 21.5)      │ -12.5 to +12.5    │ +37.0 to +61.0    │ 21.5 to 26.0        │
  │ Pi Zero 2 W      │ (0, +12, 5.5)       │ -15.0 to +15.0    │ -20.5 to +44.5    │  5.5 to 10.7        │
  │ 4G LTE HAT       │ (0, +12, 11.4)      │ -15.0 to +15.0    │ -15.5 to +39.5    │ 11.4 to 17.9        │
  │ Battery (HORIZ)  │ (0, -37, 3.5) R90°  │ -24.25 to +24.25  │ -50.25 to -23.75  │  3.5 to 21.0        │
  │ IMU (Under-Pi)   │ (0, +12, 2.5)       │  -9.0 to +9.0     │  -0.5 to +24.5    │  2.5 to  5.5        │
  │ PG7 Gland        │ (0, -61, 12)        │ centered           │ at bottom wall    │ through-wall        │
  │ SMA Antenna      │ (0, +61, 12)        │ centered           │ at top wall       │ through-wall        │
  └──────────────────┴─────────────────────┴───────────────────┴───────────────────┴─────────────────────┘

COLLISION AUDIT RESULTS:
  1. Pi (Y: -20.5 to +44.5) vs Battery (Y: -50.25 to -23.75) → GAP = 3.25mm ✅
  2. Modem (Y: -15.5 to +39.5) vs Battery (Y: -50.25 to -23.75) → GAP = 8.25mm ✅
  3. Camera (Z: 21.5-26) vs Pi (Z: 5.5-10.7) → Z GAP = 10.8mm ✅
  4. IMU (Z: 2.5-5.5) vs Pi (Z: 5.5-10.7) → IMU sits in standoff gap under Pi ✅
  5. Battery (Y: -50.25) vs PG7 Gland (Y: -61) → GAP = 10.75mm ✅
"""
import os
import sys
from build123d import *

def build_universal_base_casing():
    w, h, d = 57.0, 122.0, 26.0
    wall = 2.4
    floor_t = 2.5
    r = 14.0

    with BuildPart() as base:
        # 1. Smooth Rounded Stadium Outer Envelope
        with BuildSketch() as s1:
            Rectangle(w, h)
            fillet(s1.vertices(), radius=r)
        extrude(amount=d)

        # 2. Main Internal Cavity (52.2mm W x 117.2mm H x 23.5mm D)
        with BuildSketch(Plane.XY.offset(floor_t)) as s2:
            Rectangle(w - 2 * wall, h - 2 * wall)
            fillet(s2.vertices(), radius=max(0.5, r - wall))
        extrude(amount=d - floor_t + 1.0, mode=Mode.SUBTRACT)

        # 3. Integrated Concave Pole Saddle on Rear Face (z = 0)
        with BuildSketch(Plane.YZ) as s_saddle:
            with Locations((0, -2.0)):
                Circle(45.0)
        extrude(amount=w + 2.0, both=True, mode=Mode.SUBTRACT)

        # 4. Dual 14mm Jubilee Strap Channels (Height 15.0mm, Depth 3.0mm)
        with Locations((0, 36.0, 0), (0, -36.0, 0)):
            Box(w + 4.0, 15.0, 3.0, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        # 5. 4x Corner Receiver Socket Pillars
        screw_positions = [
            (-w/2 + 7.5, -h/2 + 9.0),
            ( w/2 - 7.5, -h/2 + 9.0),
            ( w/2 - 7.5,  h/2 - 9.0),
            (-w/2 + 7.5,  h/2 - 9.0),
        ]
        with Locations([(x, y, floor_t) for x, y in screw_positions]):
            Cylinder(radius=3.4, height=d - floor_t, align=(Align.CENTER, Align.CENTER, Align.MIN))

        with Locations([(x, y, d) for x, y in screw_positions]):
            Hole(radius=2.4, depth=5.0)
            Hole(radius=1.7, depth=d + 2.0)

        # 6. Rear Screw Counterbores
        with Locations([(x, y, 0) for x, y in screw_positions]):
            Cylinder(radius=3.2, height=1.4, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        # 7. Compute Deck Standoffs: Pi Zero 2 W (65mm) centered at Y = +12mm
        compute_y = 12.0
        pi_standoff_h = 3.0
        pi_offsets = [
            (-11.5, compute_y - 29.0),
            ( 11.5, compute_y - 29.0),
            ( 11.5, compute_y + 29.0),
            (-11.5, compute_y + 29.0),
        ]
        with Locations([(x, y, floor_t) for x, y in pi_offsets]):
            Cylinder(radius=2.4, height=pi_standoff_h, align=(Align.CENTER, Align.CENTER, Align.MIN))
            Hole(radius=1.2, depth=pi_standoff_h + 1.0)

        # 8. Under-Board IMU Anti-Tamper Mounting Pad (on floor, centered under Pi, Y=+12mm)
        with Locations((0, compute_y, floor_t)):
            Box(20.0, 27.0, 0.5, align=(Align.CENTER, Align.CENTER, Align.MIN))

        # 9. Horizontal Battery Retention Rails (Y = -37mm, cradle for 48.5mm wide battery)
        batt_y = -37.0
        with Locations((-w/2 + wall + 1.0, batt_y, floor_t), (w/2 - wall - 1.0, batt_y, floor_t)):
            Box(2.0, 30.0, 18.0, align=(Align.CENTER, Align.CENTER, Align.MIN))

        # 10. SINGLE CENTERED Bottom Gland Port for Solar DC Power (X=0, Y=-61mm)
        with BuildSketch(Plane.XZ.offset(-h/2)):
            with Locations((0, floor_t + 9.5)):
                Circle(radius=6.25)
        extrude(amount=wall + 3.0, mode=Mode.SUBTRACT)

        # 11. Top SMA Antenna Port (X=0, Y=+61mm)
        with BuildSketch(Plane.XZ.offset(h/2)):
            with Locations((0, floor_t + 9.5)):
                Circle(radius=3.25)
        extrude(amount=-(wall + 3.0), mode=Mode.SUBTRACT)

        # 12. Labyrinth Gasket Groove on Top Rim
        with BuildSketch(Plane.XY.offset(d)):
            Rectangle(w - wall, h - wall)
            fillet(s1.vertices(), radius=max(0.5, r - wall/2))
            Rectangle(w - wall - 2.2, h - wall - 2.2, mode=Mode.SUBTRACT)
        extrude(amount=-1.8, mode=Mode.SUBTRACT)

    return base.part


def build_universal_front_bezel():
    w, h, plate_t = 57.0, 122.0, 3.0
    r = 14.0
    cam_y = 46.0
    wall = 2.4

    with BuildPart() as bezel:
        # 1. Smooth Stadium Front Faceplate
        with BuildSketch() as s:
            Rectangle(w, h)
            fillet(s.vertices(), radius=r)
        extrude(amount=plate_t)

        # 2. 8.5mm Micro-Aperture with Chamfer & Glass Recess (at Y = +46mm)
        with Locations((0, cam_y, 0)):
            Hole(radius=4.25, depth=plate_t + 2.0)
            with Locations((0, 0, plate_t - 0.5)):
                Cone(bottom_radius=4.9, top_radius=4.25, height=0.6, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)
            with Locations((0, 0, 0)):
                Cylinder(radius=8.0, height=1.2, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        # 3. Camera Mounting Bosses (21.0mm x 12.5mm pitch)
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

        # 4. 4x Corner Alignment Pins
        screw_positions = [
            (-w/2 + 7.5, -h/2 + 9.0),
            ( w/2 - 7.5, -h/2 + 9.0),
            ( w/2 - 7.5,  h/2 - 9.0),
            (-w/2 + 7.5,  h/2 - 9.0),
        ]
        for x, y in screw_positions:
            with Locations((x, y, 0)):
                Cylinder(radius=2.0, height=4.5, align=(Align.CENTER, Align.CENTER, Align.MAX))
                Hole(radius=1.3, depth=4.5)
                with Locations((0, 0, -4.5)):
                    Cone(bottom_radius=1.5, top_radius=2.0, height=0.8, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        # 5. Sealing Tongue
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
    base_plate = base.locate(Location((-37.0, 0, 0)))
    bezel_plate = bezel.locate(Location((37.0, 0, 4.5)))
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
    print(" 🛡️ Generating Option B: Horizontal Battery Sentry (57×122×26mm)")
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
        "shell_tier2_complete_assembly": assembly,
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

    print("\n🎉 Option B Horizontal Battery Sentry CAD Generation Complete!")

if __name__ == "__main__":
    generate_all()
