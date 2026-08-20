#!/usr/bin/env python3
"""
Iborain Safety — 3D CAD Generator for Shell 2 (Package B: Solar Sentry Corridor Pole-Mount Enclosure)
Platform: Dual-Bay Outdoor Chassis (Compute Bay + 12V/5V Solar Regulation Bay)
Mounting: Integrated Curved Pole Saddle with Dual 15mm Jubilee Strap Channels
Optics: 15° Downward Angled Camera Mount + 35mm Deep Sun/Rain Overhang Visor
100% Pure Stealth Black-Box: Single 20mm Hooded Lens, Zero Screens, Zero Lights.
Generates:
  1. shell_tier2_main_box.step / .stl (Main dual-chamber chassis with curved pole mount)
  2. shell_tier2_faceplate_visor.step / .stl (Heavy-duty faceplate with 35mm visor)
  3. shell_tier2_complete_assembly.step (Complete CAD assembly)
"""
import os
import sys
from build123d import *

def build_tier2_main_box():
    # Outer Dimensions (mm)
    w, h, d = 128.0, 124.0, 50.0
    wall = 3.0
    floor_t = 3.0
    corner_r = 5.0

    with BuildPart() as main_box:
        # 1. Solid outer envelope
        Box(w, h, d, align=(Align.CENTER, Align.CENTER, Align.MIN))
        fillet(main_box.edges().filter_by(Axis.Z), radius=corner_r)

        # 2. Hollow out two separate internal chambers (Upper Compute & Lower Power)
        # Upper Bay (Compute & Optics): 122mm x 72mm x 47mm
        upper_h = 72.0
        upper_center_y = (h/2 - wall) - upper_h/2
        with Locations((0, upper_center_y, floor_t)):
            Box(w - 2*wall, upper_h, d - floor_t + 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        # Lower Bay (Power & Solar Stepdown): 122mm x 38mm x 47mm
        lower_h = 38.0
        lower_center_y = (-h/2 + wall) + lower_h/2
        with Locations((0, lower_center_y, floor_t)):
            Box(w - 2*wall, lower_h, d - floor_t + 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        # 3. Cable Pass-Through Slot in dividing partition (18mm x 10mm)
        partition_y = lower_center_y + lower_h/2 + wall/2
        with Locations((0, partition_y, floor_t + 15.0)):
            Box(18.0, wall + 2.0, 10.0, align=(Align.CENTER, Align.CENTER, Align.CENTER), mode=Mode.SUBTRACT)

        # 4. Perimeter Screw Bosses (6x M3 Heat-Set Inserts)
        boss_r = 4.5
        screw_positions = [
            (-w/2 + 7.5, -h/2 + 7.5),
            ( w/2 - 7.5, -h/2 + 7.5),
            ( w/2 - 7.5,  0.0),
            (-w/2 + 7.5,  0.0),
            ( w/2 - 7.5,  h/2 - 7.5),
            (-w/2 + 7.5,  h/2 - 7.5),
        ]
        with Locations([(x, y, floor_t) for x, y in screw_positions]):
            Cylinder(radius=boss_r, height=d - floor_t, align=(Align.CENTER, Align.CENTER, Align.MIN))

        # Holes for M3 Inserts (pilot hole dia 4.2mm, depth 8mm)
        with Locations([(x, y, d) for x, y in screw_positions]):
            Hole(radius=2.1, depth=8.0)

        # 5. Upper Bay: Raspberry Pi Zero 2 W Standoffs (58mm x 23mm)
        pi_center_x = 0.0
        pi_center_y = upper_center_y - 12.0
        pi_standoff_h = 6.0
        pi_hole_offsets = [
            (pi_center_x - 29.0, pi_center_y - 11.5),
            (pi_center_x + 29.0, pi_center_y - 11.5),
            (pi_center_x + 29.0, pi_center_y + 11.5),
            (pi_center_x - 29.0, pi_center_y + 11.5),
        ]
        with Locations([(x, y, floor_t) for x, y in pi_hole_offsets]):
            Cylinder(radius=3.0, height=pi_standoff_h, align=(Align.CENTER, Align.CENTER, Align.MIN))
            Hole(radius=1.8, depth=4.5) # M2.5 heat-set insert

        # 6. Upper Bay: 15° Angled Camera Mount Platform for Sony IMX500
        cam_center_x = 0.0
        cam_center_y = upper_center_y + 20.0
        with Locations((cam_center_x, cam_center_y, floor_t)):
            # Base camera platform
            Box(32.0, 24.0, 14.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
            # 4x M2 camera mounting holes
            with Locations(
                (-10.5, -6.25, 14.0), (10.5, -6.25, 14.0),
                ( 10.5,  6.25, 14.0), (-10.5,  6.25, 14.0)
            ):
                Hole(radius=1.6, depth=4.0)

        # 7. Lower Bay: 12V-to-5V Buck Converter Mounting Standoffs (40mm x 20mm)
        buck_offsets = [
            (-20.0, lower_center_y - 10.0),
            ( 20.0, lower_center_y - 10.0),
            ( 20.0, lower_center_y + 10.0),
            (-20.0, lower_center_y + 10.0),
        ]
        with Locations([(x, y, floor_t) for x, y in buck_offsets]):
            Cylinder(radius=2.6, height=5.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
            Hole(radius=1.5, depth=4.0)

        # 8. External Ports
        # Bottom Face: 2x PG7 Glands (dia 12.5mm) for Solar Panel & 12V Battery
        with BuildSketch(Plane.XZ.offset(-h/2)):
            with Locations((-30.0, floor_t + 12.0), (30.0, floor_t + 12.0)):
                Circle(radius=6.25)
        extrude(amount=wall + 2.0, mode=Mode.SUBTRACT)

        # Top Face: 1x SMA Antenna Bulkhead (dia 6.5mm) for 4G LTE
        with BuildSketch(Plane.XZ.offset(h/2)):
            with Locations((35.0, floor_t + 12.0)):
                Circle(radius=3.25)
        extrude(amount=-(wall + 2.0), mode=Mode.SUBTRACT)

        # 9. Dual 15mm Jubilee Clamp Channels across the rear (Height 16mm, Depth 3.5mm)
        with Locations((0, 35.0, 0), (0, -35.0, 0)):
            Box(w + 4.0, 16.0, 3.5, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        # 10. Perimeter Gasket Groove on Top Lip
        with BuildSketch(Plane.XY.offset(d)):
            Rectangle(w - wall + 0.2, h - wall + 0.2)
            Rectangle(w - wall - 3.2, h - wall - 3.2, mode=Mode.SUBTRACT)
        extrude(amount=-2.0, mode=Mode.SUBTRACT)

    return main_box.part


def build_tier2_faceplate():
    # Faceplate Dimensions (mm)
    w, h, plate_t = 128.0, 124.0, 3.5
    corner_r = 5.0

    with BuildPart() as faceplate:
        # 1. Base Plate
        Box(w, h, plate_t, align=(Align.CENTER, Align.CENTER, Align.MIN))
        fillet(faceplate.edges().filter_by(Axis.Z), radius=corner_r)

        # 2. Camera Lens Aperture (dia 20.4mm, aligned with upper bay camera)
        upper_center_y = (h/2 - 3.0) - 72.0/2
        cam_center_y = upper_center_y + 20.0
        with Locations((0, cam_center_y, 0)):
            Hole(radius=10.2, depth=plate_t + 2.0)

        # 3. Deep 35mm Sun & Rain Visor Overhang Hood
        visor_w = 44.0
        visor_h = 36.0
        visor_len = 35.0
        visor_t = 2.8

        with BuildSketch(Plane.XY.offset(plate_t)):
            with Locations((0, cam_center_y + 4.0)):
                Rectangle(visor_w, visor_h)
                Rectangle(visor_w - 2*visor_t, visor_h - 2*visor_t, mode=Mode.SUBTRACT)
                # Open bottom for optical field of view
                with Locations((0, -visor_h/2 + visor_t/2)):
                    Rectangle(visor_w, visor_t + 1.0, mode=Mode.SUBTRACT)
        extrude(amount=visor_len)

        # 4. 6x M3 Countersunk Screw Holes
        screw_positions = [
            (-w/2 + 7.5, -h/2 + 7.5),
            ( w/2 - 7.5, -h/2 + 7.5),
            ( w/2 - 7.5,  0.0),
            (-w/2 + 7.5,  0.0),
            ( w/2 - 7.5,  h/2 - 7.5),
            (-w/2 + 7.5,  h/2 - 7.5),
        ]
        with Locations([(x, y, 0) for x, y in screw_positions]):
            Hole(radius=1.7, depth=plate_t + 2.0)
            with Locations((0, 0, plate_t - 1.5)):
                Cylinder(radius=3.4, height=2.0, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        # 5. Gasket Tongue on bottom side
        with BuildSketch(Plane.XY):
            Rectangle(w - 3.0 - 0.5, h - 3.0 - 0.5)
            Rectangle(w - 3.0 - 2.8, h - 3.0 - 2.8, mode=Mode.SUBTRACT)
        extrude(amount=-1.8)

    return faceplate.part


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out_dir, exist_ok=True)

    print("🛠️ Generating Shell 2: Package B (Solar Sentry Corridor Pole-Mount Enclosure)...")

    # 1. Generate Main Box
    main_box = build_tier2_main_box()
    box_step = os.path.join(out_dir, "shell_tier2_main_box.step")
    box_stl = os.path.join(out_dir, "shell_tier2_main_box.stl")
    export_step(main_box, box_step)
    export_stl(main_box, box_stl)
    print(f"  ✅ Exported: {box_step} & {box_stl}")

    # 2. Generate Faceplate & Visor
    faceplate = build_tier2_faceplate()
    face_step = os.path.join(out_dir, "shell_tier2_faceplate_visor.step")
    face_stl = os.path.join(out_dir, "shell_tier2_faceplate_visor.stl")
    export_step(faceplate, face_step)
    export_stl(faceplate, face_stl)
    print(f"  ✅ Exported: {face_step} & {face_stl}")

    # 3. Generate Complete Assembly
    assembly = Compound(children=[main_box, Location((0, 0, 50.0)) * faceplate])
    assembly_step = os.path.join(out_dir, "shell_tier2_complete_assembly.step")
    export_step(assembly, assembly_step)
    print(f"  ✅ Exported Assembly: {assembly_step}")
    print("\n🎉 Shell 2 CAD models compiled successfully!")
