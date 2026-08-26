#!/usr/bin/env python3
"""
Hardware Smoke Test for Iborain Safety Edge Sentry on Raspberry Pi Zero 2 W.
100% Pure Stealth Architecture (Zero LEDs, Zero Screens, Pure Optical Intelligence):
1. I2C Bus & Anti-Tamper: MPU-6500 6-Axis Accelerometer/Gyro (0x68/0x69)
2. Camera Vision Pipeline: Sony IMX500 AI Camera (On-Sensor Neural DSP & ROI Detection)
"""
import time
import sys
import subprocess

print("==================================================")
print("  🛡️ Iborain Safety Edge Sentry Hardware Smoke Test")
print("  100% Pure Stealth Black-Box Architecture")
print("==================================================")

# 1. Test I2C Bus (MPU-6500 Anti-Tamper)
print("\n[1/2] Scanning I2C Bus for Anti-Tamper Sensor...")
try:
    import smbus2
    bus = smbus2.SMBus(1)
    found = []
    for addr in range(0x03, 0x78):
        try:
            bus.read_byte(addr)
            found.append(hex(addr))
        except Exception:
            pass
    print(f"  Found I2C devices at: {found}")
    if "0x68" in found or "0x69" in found:
        print("  ✅ MPU-6500 6-Axis IMU (Anti-Tamper & Vibration) detected (0x68/0x69)")
    else:
        print("  ℹ️ No MPU-6500 at 0x68/0x69 (verify wiring to SDA Pin 3, SCL Pin 5)")
except Exception as e:
    print(f"  ⚠️ I2C scan skipped or smbus2 not installed: {e}")

# 2. Test Camera Capture Pipeline (Sony IMX500 / Pi AI Cam)
print("\n[2/2] Testing Neural Camera Capture Pipeline (Sony IMX500)...")
try:
    cam_tool = "rpicam-still" if subprocess.run(["which", "rpicam-still"], capture_output=True).returncode == 0 else "libcamera-still"
    res = subprocess.run([cam_tool, "--list-cameras"], capture_output=True, text=True, timeout=5)
    output = (res.stdout + res.stderr).strip()
    if "Available cameras" in output and "No cameras available" not in output:
        print(f"  ✅ Camera sensor detected via {cam_tool}:\n{output}")
    else:
        print(f"  ℹ️ {cam_tool} returned no active camera (verify ribbon cable to CSI port):\n  {output}")
except Exception as e:
    print(f"  ⚠️ Camera test command error: {e}")

print("\n==================================================")
print("  🎉 Hardware Smoke Test Complete!")
print("==================================================")
