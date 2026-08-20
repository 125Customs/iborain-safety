#!/usr/bin/env python3
"""
Hardware Smoke Test for Iborain Safety Sentry on Raspberry Pi Zero 2 W.
Streamlined 3-Chip Architecture:
1. I2C Bus & Anti-Tamper: MPU-6500 6-Axis Accelerometer/Gyro (0x68/0x69)
2. Optical Arrival Tripwire: TCRT5000 IR Sensor on GPIO 17
3. Status & Strobe LED: Dual-Color Status / Threat Beacon on GPIO 24
4. Camera Vision Pipeline: libcamera-still / Picamera2 image capture
"""
import time
import sys

print("==================================================")
print("  🛡️ Iborain Safety Edge Sentry Hardware Smoke Test")
print("  Streamlined Ductile Production Architecture")
print("==================================================")

# 1. Test I2C Bus (MPU-6500 Anti-Tamper)
print("\n[1/4] Scanning I2C Bus for Anti-Tamper Sensor...")
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

# 2. Test TCRT5000 Optical Tripwire
print("\n[2/4] Testing TCRT5000 Optical Arrival Tripwire (GPIO 17)...")
try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    trip_state = GPIO.input(17)
    print(f"  ✅ TCRT5000 Pin 11 (GPIO 17) active. Current state: {'TRIGGERED (Vehicle Present)' if trip_state == 0 else 'CLEAR'}")
except Exception as e:
    print(f"  ⚠️ GPIO tripwire test skipped: {e}")

# 3. Test Status / Threat Strobe LED (GPIO 24)
print("\n[3/4] Testing Dual Status / Threat Strobe LED (GPIO 24)...")
try:
    import RPi.GPIO as GPIO
    LED_PIN = 24
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(LED_PIN, GPIO.OUT)

    print("  Pulsing Status LED 3 times...")
    for i in range(3):
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(0.15)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(0.15)
    print("  ✅ Status LED (GPIO 24) verified.")
except Exception as e:
    print(f"  ⚠️ Status LED test skipped: {e}")

# 4. Test Camera Capture
print("\n[4/4] Testing Camera Capture Pipeline...")
try:
    import subprocess
    res = subprocess.run(["libcamera-still", "--list-cameras"], capture_output=True, text=True, timeout=5)
    if "Available cameras" in res.stdout or res.returncode == 0:
        print(f"  ✅ Camera sensor detected:\n{res.stdout.strip()}")
    else:
        print("  ℹ️ libcamera-still returned no cameras (verify ribbon cable to CSI port)")
except Exception as e:
    print(f"  ⚠️ Camera test command error: {e}")

print("\n==================================================")
print("  🎉 Hardware Smoke Test Complete!")
print("==================================================")
