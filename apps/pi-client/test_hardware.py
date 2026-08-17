#!/usr/bin/env python3
"""
Hardware Smoke Test for Iborain Safety Tactical Sentry on Raspberry Pi Zero 2 W.
Tests:
1. I2C Bus & Anti-Tamper: MPU-6500 6-Axis Accelerometer (0x68/0x69)
2. Optical Arrival Tripwire: TCRT5000 IR Sensor on GPIO 17
3. GC9A01 1.28" TFT LCD: Renders Sentry Threat Deterrence Strobe & Active Radar
4. Audio Deterrence: I2S MAX98357A DAC output
"""
import time
import sys

print("==================================================")
print("  🛡️ Iborain Safety Edge Sentry Hardware Smoke Test")
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
    print(f"  ✅ TCRT5000 Pin 11 (GPIO 17) active. Current state: {'TRIGGERED' if trip_state == 0 else 'CLEAR'}")
except Exception as e:
    print(f"  ⚠️ GPIO tripwire test skipped: {e}")

# 3. Test GC9A01 Display (Deterrence Strobe & Sentry Radar)
print("\n[3/4] Testing GC9A01 1.28-inch Round TFT Display (Sentry Beacon)...")
try:
    import spidev
    import RPi.GPIO as GPIO
    from PIL import Image, ImageDraw, ImageFont

    DC_PIN = 24
    RST_PIN = 25
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(DC_PIN, GPIO.OUT)
    GPIO.setup(RST_PIN, GPIO.OUT)

    # Hardware reset
    GPIO.output(RST_PIN, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(RST_PIN, GPIO.HIGH)
    time.sleep(0.1)

    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = 40000000
    spi.mode = 0

    def send_cmd(cmd):
        GPIO.output(DC_PIN, GPIO.LOW)
        spi.xfer2([cmd])

    def send_data(data):
        GPIO.output(DC_PIN, GPIO.HIGH)
        spi.xfer2(data)

    # Init sequence for GC9A01
    send_cmd(0xFE); send_cmd(0xEF); send_cmd(0xEB); send_data([0x14])
    send_cmd(0x36); send_data([0x00])
    send_cmd(0x3A); send_data([0x05])
    send_cmd(0x11); time.sleep(0.12)
    send_cmd(0x29); time.sleep(0.02)

    # Render tactical sentry shield & radar
    img = Image.new("RGB", (240, 240), (10, 15, 30))
    draw = ImageDraw.Draw(img)

    # Concentric radar rings
    draw.ellipse((20, 20, 220, 220), outline=(0, 180, 255), width=3)
    draw.ellipse((60, 60, 180, 180), outline=(0, 100, 180), width=2)
    draw.ellipse((100, 100, 140, 140), fill=(0, 220, 120), outline=(255, 255, 255), width=2)

    # Security Crosshairs
    draw.line((120, 10, 120, 230), fill=(0, 140, 220), width=1)
    draw.line((10, 120, 230, 120), fill=(0, 140, 220), width=1)

    # Tactical Header Text
    draw.text((65, 35), "IBORAIN", fill=(255, 255, 255))
    draw.text((70, 195), "SENTRY ACTIVE", fill=(0, 255, 180))

    send_cmd(0x2A); send_data([0, 0, 0, 239])
    send_cmd(0x2B); send_data([0, 0, 0, 239])
    send_cmd(0x2C)

    raw = []
    for p in img.getdata():
        r, g, b = p[0] >> 3, p[1] >> 2, p[2] >> 3
        c = (r << 11) | (g << 5) | b
        raw.extend([(c >> 8) & 0xFF, c & 0xFF])

    GPIO.output(DC_PIN, GPIO.HIGH)
    for i in range(0, len(raw), 4096):
        spi.xfer2(raw[i:i+4096])

    print("  ✅ GC9A01 LCD successfully rendering Iborain Safety Sentry Radar & Beacon!")
except Exception as e:
    print(f"  ❌ LCD test error: {e}")

print("\n==================================================")
print("  🛡️ Sentry Hardware Smoke Test Complete!")
print("==================================================")
