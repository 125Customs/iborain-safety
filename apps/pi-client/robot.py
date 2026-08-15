#!/usr/bin/env python3
"""
Pixel Bot / SmartB0t Physical Client for Raspberry Pi Zero 2 W.
Connects to apps/backend over WebSocket, streams camera frames (RPi AI Camera) & mic audio,
plays returned Gemini 24kHz audio via I2S / ALSA, and renders eye expressions on GC9A01 LCD.
"""
import os
import sys
import json
import time
import struct
import asyncio
import websockets

BACKEND_URL = os.getenv("BACKEND_URL", "ws://192.168.1.100:8080")
DEVICE_ID = os.getenv("DEVICE_ID", "pi-robot")
TOKEN = os.getenv("DEVICE_TOKEN", "local-secret")

print(f"🤖 Starting SmartB0t Client -> Connecting to {BACKEND_URL} as {DEVICE_ID}...")

async def run_robot():
    url = f"{BACKEND_URL}/?device={DEVICE_ID}&token={TOKEN}"
    while True:
        try:
            print(f"Connecting to {url}...")
            async with websockets.connect(url) as ws:
                print("✅ Connected to backend!")
                # Send hello
                await ws.send(json.dumps({
                    "type": "hello",
                    "proto": 1,
                    "deviceId": DEVICE_ID,
                    "fw": "pi-0.1.0"
                }))

                async for message in ws:
                    if isinstance(message, str):
                        data = json.loads(message)
                        msg_type = data.get("type")
                        if msg_type == "hello_ack":
                            print(f"👋 Handshake acknowledged: session {data.get('sessionId', '')[:8]}")
                        elif msg_type == "control":
                            expression = data.get("expression")
                            action = data.get("action")
                            print(f"🎭 Robot Command -> Expression: {expression} | Action: {action}")
                        elif msg_type == "interrupted":
                            print("⚡ User interrupted -> Barge-in flush!")
                        elif msg_type == "bye":
                            print(f"🚪 Session closed by server ({data.get('reason')})")
                            break
                    elif isinstance(message, bytes):
                        # Binary frame: [1B type][8B timestamp][payload]
                        if len(message) >= 9:
                            frame_type = message[0]
                            if frame_type == 0x11: # AudioOut (24kHz PCM)
                                audio_payload = message[9:]
                                # Write to ALSA speaker playback stream
        except Exception as e:
            print(f"⚠️ Connection error: {e}. Reconnecting in 3s...")
            await asyncio.sleep(3)

if __name__ == "__main__":
    try:
        asyncio.run(run_robot())
    except KeyboardInterrupt:
        print("\nRobot stopped.")
