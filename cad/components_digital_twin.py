#!/usr/bin/env python3
"""
Iborain Safety — 3D CAD Digital Twins of Physical Hardware Components
Generates exact 1:1 scale solid CAD geometry (.step and .stl) for all 8 physical components:
  1. Raspberry Pi Zero 2 W (65.0 x 30.0 x 5.2mm, RP3A0 SoC, 4x M2.5 mounting holes)
  2. Raspberry Pi AI Camera / Sony IMX500 (25.0 x 24.0 x 4.5mm, 8.5mm lens barrel, 4x M2.0 holes)
  3. Quectel 4G LTE Modem Module (55.0 x 30.0 x 6.5mm, SIM slot, U.FL RF)
  4. InvenSense ICM-20948 / MPU-6500 IMU Breakout (18.0 x 25.0 x 3.0mm, 2x M2.5 holes)
  5. Bestfire 5V / 3.7V 1350mAh USB Type-C Rechargeable Li-ion Battery (48.5 x 26.5 x 17.5mm)
  6. AR Coated Optical Glass Disc Window (16.0mm Dia x 1.2mm T)
  7. IP68 PG7 Compression Cable Gland (12.5mm Thread Dia x 28.0mm L)
  8. SMA Female to IPEX 4G Antenna Bulkhead (6.5mm Thread Dia x 15.0mm L)
"""
import os
import sys
from build123d import *

def build_pi_zero_2w():
    """Raspberry Pi Zero 2 W (65.0 x 30.0 x 5.2mm)"""
    w, h, pcb_t = 30.0, 65.0, 1.4
    r = 3.0 # corner radius
    with BuildPart() as pi:
        # PCB Base
        with BuildSketch() as s:
            Rectangle(w, h)
            fillet(s.vertices(), radius=r)
        extrude(amount=pcb_t)
        
        # 4x M2.5 Mounting Holes (58.0 x 23.0mm pitch, 2.75mm dia)
        with Locations([(-11.5, -29.0), (11.5, -29.0), (11.5, 29.0), (-11.5, 29.0)]):
            Hole(radius=1.375, depth=pcb_t + 1.0)
            
        # RP3A0-AU Broadcom Quad-Core SoC (15.0 x 15.0 x 1.2mm)
        with Locations((0, 5.0, pcb_t)):
            Box(15.0, 15.0, 1.2, align=(Align.CENTER, Align.CENTER, Align.MIN))
            
        # MicroSD Card Slot (Underside left edge)
        with Locations((0, -32.5, 0)):
            Box(12.0, 14.0, 1.4, align=(Align.CENTER, Align.MAX, Align.MAX))
            
        # 2x Micro-USB Ports (PWR & OTG, right edge)
        with Locations((w/2, -10.5, pcb_t), (w/2, 3.5, pcb_t)):
            Box(5.6, 7.5, 2.8, align=(Align.MAX, Align.CENTER, Align.MIN))
            
        # Mini-HDMI Port
        with Locations((w/2, 18.0, pcb_t)):
            Box(7.2, 11.2, 3.2, align=(Align.MAX, Align.CENTER, Align.MIN))
            
        # CSI-2 Camera FFC Connector (Top edge)
        with Locations((0, 32.5, pcb_t)):
            Box(17.0, 4.0, 1.5, align=(Align.CENTER, Align.MAX, Align.MIN))
    return pi.part

def build_sony_imx500_camera():
    """Raspberry Pi AI Camera / Sony IMX500 (25.0 x 24.0 x 4.5mm)"""
    w, h, pcb_t = 25.0, 24.0, 1.0
    with BuildPart() as cam:
        # PCB Base
        Box(w, h, pcb_t, align=(Align.CENTER, Align.CENTER, Align.MIN))
        
        # 4x M2.0 Mounting Holes (21.0 x 12.5mm pitch, 2.2mm dia)
        with Locations([(-10.5, -6.25), (10.5, -6.25), (10.5, 6.25), (-10.5, 6.25)]):
            Hole(radius=1.1, depth=pcb_t + 1.0)
            
        # Sony IMX500 Neural Sensor Package (8.0 x 8.0 x 0.8mm)
        with Locations((0, 0, pcb_t)):
            Box(8.0, 8.0, 0.8, align=(Align.CENTER, Align.CENTER, Align.MIN))
            
        # Cylindrical Lens Barrel (8.5mm OD x 3.5mm protrusion)
        with Locations((0, 0, pcb_t)):
            Cylinder(radius=4.25, height=3.5, align=(Align.CENTER, Align.CENTER, Align.MIN))
            # Optical Glass Aperture Pupil
            with Locations((0, 0, 3.5)):
                Cylinder(radius=3.0, height=0.5, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)
                
        # CSI-2 22-pin FFC Receptacle on Rear
        with Locations((0, -10.5, 0)):
            Box(12.0, 3.0, 1.2, align=(Align.CENTER, Align.CENTER, Align.MAX))
    return cam.part

def build_bestfire_battery():
    """Bestfire 5V / 3.7V 1350mAh USB Type-C Rechargeable Li-ion Battery (48.5 x 26.5 x 17.5mm)"""
    w, h, d = 26.5, 48.5, 17.5
    r = 3.5
    with BuildPart() as batt:
        # Main Prismatic Battery Body
        with BuildSketch() as s:
            Rectangle(w, h - 3.5)
            fillet(s.vertices(), radius=r)
        extrude(amount=d)
        
        # Top Terminals & USB-C Port Header
        with Locations((0, (h - 3.5)/2, d/2)):
            Box(w - 2.0, 3.5, d - 2.0, align=(Align.CENTER, Align.MIN, Align.CENTER))
            
        # USB Type-C Charging Receptacle (Side/Top) - Flush Recessed (Zero Protrusion)
        with Locations((0, (h - 3.5)/2 + 1.5, d/2)):
            Box(8.9, 3.2, 3.2, align=(Align.CENTER, Align.CENTER, Align.CENTER), mode=Mode.SUBTRACT)
    return batt.part

def build_4g_lte_modem():
    """Quectel 4G LTE / SIM Modem Module (55.0 x 30.0 x 6.5mm)"""
    w, h, pcb_t = 30.0, 55.0, 1.2
    with BuildPart() as modem:
        # PCB Base
        Box(w, h, pcb_t, align=(Align.CENTER, Align.CENTER, Align.MIN))
        
        # 4G LTE Metallic RF Shielding Can (26.0 x 24.0 x 2.8mm)
        with Locations((0, 8.0, pcb_t)):
            Box(26.0, 24.0, 2.8, align=(Align.CENTER, Align.CENTER, Align.MIN))
            
        # Push-Push Nano SIM Card Tray (12.5 x 15.0 x 1.5mm)
        with Locations((0, -16.0, pcb_t)):
            Box(12.5, 15.0, 1.5, align=(Align.CENTER, Align.CENTER, Align.MIN))
            
        # U.FL / IPEX Micro RF Connector
        with Locations((10.0, 23.0, pcb_t)):
            Cylinder(radius=1.5, height=1.4, align=(Align.CENTER, Align.CENTER, Align.MIN))
    return modem.part

def build_imu_breakout():
    """InvenSense ICM-20948 / MPU-6500 IMU (18.0 x 25.0 x 3.0mm)"""
    w, h, pcb_t = 18.0, 25.0, 1.6
    with BuildPart() as imu:
        # PCB Base
        Box(w, h, pcb_t, align=(Align.CENTER, Align.CENTER, Align.MIN))
        
        # 2x M2.5 Mounting Holes (20.0mm spacing, 2.5mm dia)
        with Locations((0, -10.0), (0, 10.0)):
            Hole(radius=1.25, depth=pcb_t + 1.0)
            
        # ICM-20948 QFN MotionTracking IC (3.0 x 3.0 x 1.0mm)
        with Locations((0, 0, pcb_t)):
            Box(3.0, 3.0, 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
            
        # I2C 4-Pin Solder Header Footprint (2.54mm pitch)
        with Locations((-6.5, 0, pcb_t)):
            Box(2.5, 10.16, 1.5, align=(Align.CENTER, Align.CENTER, Align.MIN))
    return imu.part

def build_optical_glass():
    """Anti-Reflective Optical Glass Disc (16.0mm Dia x 1.2mm T)"""
    with BuildPart() as glass:
        Cylinder(radius=8.0, height=1.2, align=(Align.CENTER, Align.CENTER, Align.MIN))
    return glass.part

def build_pg7_gland():
    """IP68 PG7 Nylon Cable Gland (12.5mm Thread Dia x 28.0mm L)"""
    with BuildPart() as gland:
        # Threaded Barrel (Dia 12.5mm x 8.0mm)
        Cylinder(radius=6.25, height=8.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
        # Hex Collar (18.0mm Across Flats x 5.0mm)
        with Locations((0, 0, 8.0)):
            with BuildSketch() as s:
                RegularPolygon(radius=10.0, side_count=6)
            extrude(amount=5.0)
        # Compression Dome Nut (Dia 15.0mm x 15.0mm)
        with Locations((0, 0, 13.0)):
            Cylinder(radius=7.5, height=15.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
            # Through-Bore for Cable (Dia 5.5mm)
            Hole(radius=2.75, depth=28.0)
    return gland.part

def build_sma_bulkhead():
    """SMA Female to IPEX 4G RF Bulkhead (6.5mm Thread Dia x 15.0mm L)"""
    with BuildPart() as sma:
        # Threaded Barrel (Dia 6.35mm x 11.0mm)
        Cylinder(radius=3.175, height=11.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
        # Hex Nut & Flange (Dia 8.0mm x 4.0mm)
        with Locations((0, 0, 11.0)):
            with BuildSketch() as s:
                RegularPolygon(radius=4.5, side_count=6)
            extrude(amount=4.0)
        # Center Pin Receptacle
        Hole(radius=0.6, depth=15.0)
    return sma.part

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "components")
    os.makedirs(out_dir, exist_ok=True)
    
    print("🔬 Compiling High-Precision 3D Digital Twin Hardware Components...")
    components = {
        "digital_twin_pi_zero_2w": build_pi_zero_2w(),
        "digital_twin_sony_imx500_camera": build_sony_imx500_camera(),
        "digital_twin_bestfire_battery": build_bestfire_battery(),
        "digital_twin_4g_lte_modem": build_4g_lte_modem(),
        "digital_twin_imu_breakout": build_imu_breakout(),
        "digital_twin_optical_glass": build_optical_glass(),
        "digital_twin_pg7_gland": build_pg7_gland(),
        "digital_twin_sma_bulkhead": build_sma_bulkhead(),
    }
    
    for name, part in components.items():
        export_step(part, os.path.join(out_dir, f"{name}.step"))
        export_stl(part, os.path.join(out_dir, f"{name}.stl"))
        print(f"  • {name}.step & .stl exported")
        
    print(f"\n  ✅ All {len(components)} Digital Twin Hardware Components Exported Successfully to `cad/components/`!")
