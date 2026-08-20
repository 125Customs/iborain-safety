#!/usr/bin/env python3
"""
GC9A01 1.28-inch Round TFT LCD Display Driver & Tactical HUD Renderer.
Renders live system telemetry, IP address, scanned license plates, vehicle classifications,
and threat alerts with graceful fallback if hardware SPI is not present.
"""
import time
import socket

class SentryDisplay:
    def __init__(self, enabled=True):
        self.enabled = enabled
        self.spi = None
        self.ip_address = self._get_ip()
        
        if not self.enabled:
            return

        try:
            import spidev
            import RPi.GPIO as GPIO
            from PIL import Image, ImageDraw, ImageFont

            self.Image = Image
            self.ImageDraw = ImageDraw
            self.ImageFont = ImageFont
            self.GPIO = GPIO

            self.DC_PIN = 24
            self.RST_PIN = 25
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(self.DC_PIN, GPIO.OUT)
            GPIO.setup(self.RST_PIN, GPIO.OUT)

            # Hardware Reset
            GPIO.output(self.RST_PIN, GPIO.LOW)
            time.sleep(0.05)
            GPIO.output(self.RST_PIN, GPIO.HIGH)
            time.sleep(0.05)

            self.spi = spidev.SpiDev()
            self.spi.open(0, 0)
            self.spi.max_speed_hz = 40000000
            self.spi.mode = 0

            self._init_gc9a01()
            self.render_idle("INITIALIZING...")
            print("✅ GC9A01 1.28\" Round TFT LCD HUD initialized successfully!")
        except Exception as e:
            print(f"ℹ️ GC9A01 Display offline or SPI not available: {e}. Running in headless mode.")
            self.enabled = False

    def _get_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    def _send_cmd(self, cmd):
        self.GPIO.output(self.DC_PIN, self.GPIO.LOW)
        self.spi.xfer2([cmd])

    def _send_data(self, data):
        self.GPIO.output(self.DC_PIN, self.GPIO.HIGH)
        self.spi.xfer2(data)

    def _init_gc9a01(self):
        self._send_cmd(0xFE); self._send_cmd(0xEF)
        self._send_cmd(0xEB); self._send_data([0x14])
        self._send_cmd(0x84); self._send_data([0x40])
        self._send_cmd(0x85); self._send_data([0xFF])
        self._send_cmd(0x86); self._send_data([0xFF])
        self._send_cmd(0x87); self._send_data([0xFF])
        self._send_cmd(0x8E); self._send_data([0xFF])
        self._send_cmd(0x8F); self._send_data([0xFF])
        self._send_cmd(0x3A); self._send_data([0x05]) # RGB565 16-bit
        self._send_cmd(0x36); self._send_data([0x00]) # Orientation
        self._send_cmd(0x11); time.sleep(0.12)        # Sleep Out
        self._send_cmd(0x29); time.sleep(0.02)        # Display ON

    def _flush_image(self, img):
        if not self.enabled or not self.spi:
            return
        
        # Set column and page address
        self._send_cmd(0x2A); self._send_data([0x00, 0x00, 0x00, 0xEF])
        self._send_cmd(0x2B); self._send_data([0x00, 0x00, 0x00, 0xEF])
        self._send_cmd(0x2C)

        # Convert RGB888 to RGB565
        pixels = list(img.getdata())
        raw_data = []
        for r, g, b in pixels:
            rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
            raw_data.append((rgb565 >> 8) & 0xFF)
            raw_data.append(rgb565 & 0xFF)
        
        self.GPIO.output(self.DC_PIN, self.GPIO.HIGH)
        chunk_size = 4096
        for i in range(0, len(raw_data), chunk_size):
            self.spi.xfer2(raw_data[i:i+chunk_size])

    def render_idle(self, status="SCANNING..."):
        if not self.enabled: return
        img = self.Image.new("RGB", (240, 240), (6, 12, 8))
        draw = self.ImageDraw.Draw(img)

        # Outer Tactical Rings
        draw.ellipse((8, 8, 232, 232), outline=(16, 185, 129), width=2)
        draw.ellipse((20, 20, 220, 220), outline=(5, 70, 45), width=1)

        # Header
        draw.text((80, 30), "IBORAIN", fill=(16, 185, 129))
        draw.text((70, 50), f"IP: {self.ip_address}", fill=(156, 163, 175))
        draw.line((40, 75, 200, 75), fill=(16, 185, 129), width=1)

        # Radar Reticle
        draw.ellipse((80, 95, 160, 175), outline=(16, 185, 129), width=1)
        draw.ellipse((110, 125, 130, 145), fill=(16, 185, 129))
        draw.line((120, 85, 120, 185), fill=(16, 185, 129), width=1)
        draw.line((70, 135, 170, 135), fill=(16, 185, 129), width=1)

        # Status
        draw.text((75, 195), status, fill=(52, 211, 153))
        self._flush_image(img)

    def render_result(self, plate, vehicle_type, threat="CLEARED", latency_ms=310):
        if not self.enabled: return
        is_threat = "HOTLIST" in threat or "SUSPICIOUS" in threat
        bg_color = (25, 5, 5) if is_threat else (5, 20, 10)
        border_color = (239, 68, 68) if is_threat else (16, 185, 129)

        img = self.Image.new("RGB", (240, 240), bg_color)
        draw = self.ImageDraw.Draw(img)

        # Outer Tactical Rings
        draw.ellipse((8, 8, 232, 232), outline=border_color, width=3)

        # Title
        header_text = "🚨 HOTLIST MATCH" if is_threat else "🛡️ IBORAIN SENTRY"
        draw.text((55, 30), header_text, fill=border_color)
        draw.line((40, 55, 200, 55), fill=border_color, width=1)

        # License Plate Box
        draw.rectangle((35, 70, 205, 115), fill=(0, 0, 0), outline=border_color, width=2)
        plate_str = str(plate or "UNPLATED")
        draw.text((65, 82), plate_str, fill=(255, 255, 255))

        # Vehicle Info
        v_type_str = str(vehicle_type or "VEHICLE").upper()
        draw.text((45, 130), f"TYPE: {v_type_str[:18]}", fill=(229, 231, 235))
        draw.text((45, 150), f"VERDICT: {threat[:16]}", fill=border_color)

        # Latency / Sensor Footer
        draw.line((40, 175, 200, 175), fill=border_color, width=1)
        draw.text((60, 190), f"LATENCY: {latency_ms}ms", fill=(156, 163, 175))

        self._flush_image(img)

    def render_tamper(self):
        if not self.enabled: return
        img = self.Image.new("RGB", (240, 240), (220, 20, 20))
        draw = self.ImageDraw.Draw(img)
        draw.text((30, 80), "⚠️ TAMPER ALERT", fill=(255, 255, 255))
        draw.text((35, 110), "IMU SHOCK DETECTED", fill=(255, 255, 255))
        draw.text((45, 140), "PATROL DISPATCHED", fill=(0, 0, 0))
        self._flush_image(img)
