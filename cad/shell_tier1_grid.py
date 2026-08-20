#!/usr/bin/env python3
"""
Iborain Safety — 3D CAD Generator for Shell 1 (Package A: Grid Sentry Checkpoint Enclosure)
Platform: Raspberry Pi Zero 2 W + Sony IMX500 AI Camera + 4G LTE + MPU-6500 Anti-Tamper
100% Pure Stealth Black-Box: Single 20mm Hooded Lens Aperture, Zero Screens, Zero Lights.
Generates:
  1. shell_tier1_main_box.step / .stl (Main electronics casing with PCB standoffs)
  2. shell_tier1_faceplate_visor.step / .stl (Front faceplate with 25mm rain/sun visor)
  3. shell_tier1_complete_assembly.step (Complete CAD assembly)
"""
import os
import sys
from build123d import *

def build_tier1_main_box():
    # Outer Dimensions (mm)
    w, h, d = 92.0, 88.0, 36.0
    wall = 2.4
    floor_t = 2.4
    corner_r = 4.0

    with BuildPart() as main_box:
        # 1. Solid outer envelope
        Box(w, h, d, align=(Align.CENTER, Align.CENTER, Align.MIN))
        fillet(main_box.edges().filter_by(Axis.Z), radius=corner_r)

        # 2. Hollow out internal cavity (leaving 2.4mm walls and floor)
        cavity_w = w - 2 * wall
        cavity_h = h - 2 * wall
        cavity_d = d - floor_t + 1.0 # slight overshoot for clean top face
        with Locations((0, 0, floor_t)):
            Box(cavity_w, cavity_h, cavity_d, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        # 3. Corner Screw Bosses (for M3 Heat-Set Inserts)
        boss_r = 4.2
        corner_offsets = [
            (-w/2 + 7.0, -h/2 + 7.0),
            ( w/2 - 7.0, -h/2 + 7.0),
            ( w/2 - 7.0,  h/2 - 7.0),
            (-w/2 + 7.0,  h/2 - 7.0),
        ]
        with Locations([(x, y, floor_t) for x, y in corner_offsets]):
            Cylinder(radius=boss_r, height=d - floor_t, align=(Align.CENTER, Align.CENTER, Align.MIN))

        # 4. Corner Holes for M3 Inserts (pilot hole dia 4.2mm, depth 6.5mm)
        with Locations([(x, y, d) for x, y in corner_offsets]):
            Hole(radius=2.1, depth=6.5)

        # 5. Raspberry Pi Zero 2 W Standoffs (58mm x 23mm hole pattern)
        # Positioned in lower half of the cavity
        pi_center_x = 0.0
        pi_center_y = -12.0
        pi_standoff_h = 6.0
        pi_standoff_r = 2.8
        pi_hole_offsets = [
            (pi_center_x - 29.0, pi_center_y - 11.5),
            (pi_center_x + 29.0, pi_center_y - 11.5),
            (pi_center_x + 29.0, pi_center_y + 11.5),
            (pi_center_x - 29.0, pi_center_y + 11.5),
        ]
        with Locations([(x, y, floor_t) for x, y in pi_hole_offsets]):
            Cylinder(radius=pi_standoff_r, height=pi_standoff_h, align=(Align.CENTER, Align.CENTER, Align.MIN))
            Hole(radius=1.8, depth=4.5) # M2.5 heat-set insert

        # 6. Sony IMX500 AI Camera Standoffs (21mm x 12.5mm hole pattern)
        # Positioned in upper half of the cavity
        cam_center_x = 0.0
        cam_center_y = 22.0
        cam_standoff_h = 12.0
        cam_standoff_r = 2.4
        cam_hole_offsets = [
            (cam_center_x - 10.5, cam_center_y - 6.25),
            (cam_center_x + 10.5, cam_center_y - 6.25),
            (cam_center_x + 10.5, cam_center_y + 6.25),
            (cam_center_x - 10.5, cam_center_y + 6.25),
        ]
        with Locations([(x, y, floor_t) for x, y in cam_hole_offsets]):
            Cylinder(radius=cam_standoff_r, height=cam_standoff_h, align=(Align.CENTER, Align.CENTER, Align.MIN))
            Hole(radius=1.6, depth=4.0) # M2 heat-set insert

        # 7. MPU-6500 Anti-Tamper Mounting Platform
        with Locations((w/2 - 16.0, 0, floor_t)):
            Box(14.0, 20.0, 4.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
            with Locations((0, -6.0, 4.0), (0, 6.0, 4.0)):
                Hole(radius=1.3, depth=4.0)

        # 8. Cable & Antenna Ports
        # Bottom face: PG7 Cable Gland (dia 12.5mm) for 5V/3A DC power cable
        with BuildSketch(Plane.XZ.offset(-h/2)):
            with Locations((0, floor_t + 10.0)):
                Circle(radius=6.25)
        extrude(amount=wall + 2.0, mode=Mode.SUBTRACT)

        # Top face: SMA Female Bulkhead (dia 6.5mm) for 4G LTE High-Gain Antenna
        with BuildSketch(Plane.XZ.offset(h/2)):
            with Locations((25.0, floor_t + 10.0)):
                Circle(radius=3.25)
        extrude(amount=-(wall + 2.0), mode=Mode.SUBTRACT)

        # 9. Rear Wall Mounting Holes (4x M4 clearance holes, 60mm x 60mm spacing)
        with Locations([(-30.0, -30.0, 0), (30.0, -30.0, 0), (30.0, 30.0, 0), (-30.0, 30.0, 0)]):
            Hole(radius=2.2, depth=floor_t + 2.0)

        # 10. Perimeter Gasket Labyrinth Seal Groove (Top Lip)
        with BuildSketch(Plane.XY.offset(d)):
            Rectangle(w - wall + 0.2, h - wall + 0.2)
            Rectangle(w - wall - 2.8, h - wall - 2.8, mode=Mode.SUBTRACT)
        extrude(amount=-1.6, mode=Mode.SUBTRACT)

    return main_box.part


def build_tier1_faceplate():
    # Faceplate Dimensions (mm)
    w, h, plate_t = 92.0, 88.0, 3.0
    corner_r = 4.0

    with BuildPart() as faceplate:
        # 1. Base Faceplate Plate
        Box(w, h, plate_t, align=(Align.CENTER, Align.CENTER, Align.MIN))
        fillet(faceplate.edges().filter_by(Axis.Z), radius=corner_r)

        # 2. Camera Lens Aperture (dia 20.4mm, centered at y = 22mm)
        cam_center_y = 22.0
        with Locations((0, cam_center_y, 0)):
            Hole(radius=10.2, depth=plate_t + 2.0)

        # 3. Integrated Overhang Sun & Rain Visor Canopy (25mm overhang)
        # Built as a sleek 3-sided protective hood projecting along +Z
        visor_w = 36.0
        visor_h = 30.0
        visor_len = 25.0
        visor_t = 2.4

        with BuildSketch(Plane.XY.offset(plate_t)):
            with Locations((0, cam_center_y + 3.0)):
                # Outer horseshoe / U-profile
                Rectangle(visor_w, visor_h)
                # Hollow inner cavity
                Rectangle(visor_w - 2*visor_t, visor_h - 2*visor_t, mode=Mode.SUBTRACT)
                # Open bottom for optical field of view
                with Locations((0, -visor_h/2 + visor_t/2)):
                    Rectangle(visor_w, visor_t + 1.0, mode=Mode.SUBTRACT)
        extrude(amount=visor_len)

        # 4. Corner M3 Screw Holes with Countersink
        corner_offsets = [
            (-w/2 + 7.0, -h/2 + 7.0),
            ( w/2 - 7.0, -h/2 + 7.0),
            ( w/2 - 7.0,  h/2 - 7.0),
            (-w/2 + 7.0,  h/2 - 7.0),
        ]
        with Locations([(x, y, 0) for x, y in corner_offsets]):
            Hole(radius=1.7, depth=plate_t + 2.0) # M3 clearance
            with Locations((0, 0, plate_t - 1.2)):
                Cylinder(radius=3.2, height=2.0, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

        # 5. Mating Gasket Seal Tongue (bottom of faceplate)
        with BuildSketch(Plane.XY):
            Rectangle(w - 2.4 - 0.4, h - 2.4 - 0.4)
            Rectangle(w - 2.4 - 2.4, h - 2.4 - 2.4, mode=Mode.SUBTRACT)
        extrude(amount=-1.4)

    return faceplate.part


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out_dir, exist_ok=True)

    print("🛠️ Generating Shell 1: Package A (Grid Sentry Checkpoint Enclosure)...")
    
    # 1. Generate Main Box
    main_box = build_tier1_main_box()
    box_step = os.path.join(out_dir, "shell_tier1_main_box.step")
    box_stl = os.path.join(out_dir, "shell_tier1_main_box.stl")
    export_step(main_box, box_step)
    export_stl(main_box, box_stl)
    print(f"  ✅ Exported: {box_step} & {box_stl}")

    # 2. Generate Faceplate & Visor
    faceplate = build_tier1_faceplate()
    face_step = os.path.join(out_dir, "shell_tier1_faceplate_visor.step")
    face_stl = os.path.join(out_dir, "shell_tier1_faceplate_visor.stl")
    export_step(faceplate, face_step)
    export_stl(faceplate, face_stl)
    print(f"  ✅ Exported: {face_step} & {face_stl}")

    # 3. Generate Complete Assembly
    assembly = Compound(children=[main_box, Location((0, 0, 36.0)) * faceplate])
    assembly_step = os.path.join(out_dir, "shell_tier1_complete_assembly.step")
    export_step(assembly, assembly_step)
    print(f"  ✅ Exported Assembly: {assembly_step}")
    print("\n🎉 Shell 1 CAD models compiled successfully!")
