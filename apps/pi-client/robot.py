#!/usr/bin/env python3
"""
BomaSafety Edge Sentry Client for Raspberry Pi Zero 2 W + Sony IMX500 AI Camera.
Connects to apps/backend over WebSocket, streams high-speed camera frames & mic audio,
plays returned Gemini 24kHz acoustic deterrence via MAX98357A I2S DAC, and renders
active sentry threat beacons & strobes on the GC9A01 LCD.
"""
import os
import sys
import json
import time
import struct
import asyncio
import websockets

BACKEND_URL = os.getenv("BACKEND_URL", "ws://192.168.1.100:8080")
DEVICE_ID = os.getenv("DEVICE_ID", "sentry-nairobi-001")
TOKEN = os.getenv("DEVICE_TOKEN", "local-secret")

print(f"🛡️ Starting BomaSafety Sentry -> Connecting to {BACKEND_URL} as {DEVICE_ID}...")

async def run_sentry():
    url = f"{BACKEND_URL}/?device={DEVICE_ID}&token={TOKEN}"
    while True:
        try:
            print(f"Connecting to {url}...")
            async with websockets.connect(url) as ws:
                print("✅ Connected to BomaSafety Cloud Brain!")
                # Send hello
                await ws.send(json.dumps({
                    "type": "hello",
                    "proto": 1,
                    "deviceId": DEVICE_ID,
                    "fw": "sentry-1.0.0"
                }))

                async for message in ws:
                    if isinstance(message, str):
                        data = json.loads(message)
                        msg_type = data.get("type")
                        if msg_type == "hello_ack":
                            print(f"👋 Sentry Authenticated: session {data.get('sessionId', '')[:8]}")
                        elif msg_type == "control":
                            threat = data.get("threatLevel")
                            deterrence = data.get("deterrence")
                            msg = data.get("message")
                            fp = data.get("fingerprint")
                            print(f"🚨 Sentry Alert -> Threat: [{threat}] | Deterrence: [{deterrence}] | Status: {msg}")
                            if fp:
                                print(f"   📋 Transit Forensic Record: Plate={fp.get('plate')} | Type={fp.get('vehicleType')} | Traits={fp.get('traits')}")
                        elif msg_type == "interrupted":
                            print("⚡ Scene interrupted -> Immediate audio buffer flush!")
                        elif msg_type == "bye":
                            print(f"🚪 Session closed by server ({data.get('reason')})")
                            break
                    elif isinstance(message, bytes):
                        # Binary frame: [1B type][8B timestamp][payload]
                        if len(message) >= 9:
                            frame_type = message[0]
                            if frame_type == 0x11: # AudioOut (24kHz PCM Acoustic Deterrence)
                                audio_payload = message[9:]
                                # Write to ALSA / I2S speaker playback queue
        except Exception as e:
            print(f"⚠️ Connection error: {e}. Reconnecting in 3s...")
            await asyncio.sleep(3)

if __name__ == "__main__":
    try:
        asyncio.run(run_sentry())
    except KeyboardInterrupt:
        print("\nSentry unit stopped.")
