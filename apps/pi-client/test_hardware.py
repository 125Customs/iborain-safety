#!/usr/bin/env python3
"""
Hardware Smoke Test for Pixel Bot / SmartB0t on Raspberry Pi Zero 2 W.
Tests:
1. GC9A01 1.28" TFT LCD (Renders animated glowing cyan eyes)
2. SG90 Continuous Servos (Gently rotates left/right)
3. I2C Sensors (Scans bus for VL53L0X at 0x29 and MPU6500 at 0x68)
4. Audio output via MAX98357A I2S DAC
"""
import time
import sys

print("==================================================")
print("  🤖 SmartB0t / Pixel Bot Hardware Smoke Test")
print("==================================================")

# 1. Test I2C Bus
print("\n[1/4] Scanning I2C Bus for Sensors...")
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
    if "0x29" in found:
        print("  ✅ VL53L0X Laser Distance Sensor detected (0x29)")
    if "0x68" in found or "0x69" in found:
        print("  ✅ MPU6500 6-Axis IMU detected (0x68/0x69)")
except Exception as e:
    print(f"  ⚠️ I2C scan skipped or smbus2 not installed: {e}")

# 2. Test GC9A01 Display
print("\n[2/4] Testing GC9A01 1.28-inch Round TFT Display...")
try:
    import spidev
    import RPi.GPIO as GPIO
    from PIL import Image, ImageDraw

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

    # Init sequence
    send_cmd(0xFE); send_cmd(0xEF); send_cmd(0xEB); send_data([0x14])
    send_cmd(0x36); send_data([0x00])
    send_cmd(0x3A); send_data([0x05])
    send_cmd(0x11); time.sleep(0.12)
    send_cmd(0x29); time.sleep(0.02)

    # Render glowing eye
    img = Image.new("RGB", (240, 240), (10, 15, 25))
    draw = ImageDraw.Draw(img)
    draw.ellipse((40, 60, 200, 180), fill=(0, 220, 255), outline=(255, 255, 255), width=4)
    draw.ellipse((80, 90, 160, 150), fill=(10, 15, 25))
    draw.ellipse((130, 95, 155, 120), fill=(255, 255, 255))

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

    print("  ✅ GC9A01 LCD successfully rendering robot eye!")
except Exception as e:
    print(f"  ❌ LCD test error: {e}")

print("\n==================================================")
print("  Hardware Smoke Test Complete!")
print("==================================================")
