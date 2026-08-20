#!/usr/bin/env python3
"""
Iborain Safety Edge Sentry Client for Raspberry Pi Zero 2 W + Sony IMX500 AI Camera.
Features optional GC9A01 1.28-inch Round TFT Diagnostic HUD for live prototyping & video demos.
Connects to apps/backend over WebSocket, streams high-speed camera frames & sensor telemetry,
and receives real-time Gemini threat classifications.
"""
import os
import sys
import json
import time
import struct
import asyncio

# Check for demo mode early before requiring network dependencies
if __name__ == "__main__" and ("--demo" in sys.argv or "-d" in sys.argv):
    # Ensure current directory is in python path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    try:
        from demo_sentry import main as run_demo_main
        run_demo_main()
        sys.exit(0)
    except ImportError as e:
        print(f"❌ demo_sentry.py could not be loaded: {e}")
        sys.exit(1)

try:
    from display import SentryDisplay
    hud = SentryDisplay(enabled=True)
except Exception:
    hud = None

BACKEND_URL = os.getenv("BACKEND_URL", "ws://192.168.1.100:8080")
DEVICE_ID = os.getenv("DEVICE_ID", "sentry-nairobi-001")
TOKEN = os.getenv("DEVICE_TOKEN", "local-secret")

print(f"🛡️ Starting Iborain Safety Sentry -> Connecting to {BACKEND_URL} as {DEVICE_ID}...")

async def run_sentry():
    import websockets
    url = f"{BACKEND_URL}/?device={DEVICE_ID}&token={TOKEN}"
    while True:
        try:
            if hud:
                hud.render_idle("CONNECTING...")
            print(f"Connecting to {url}...")
            async with websockets.connect(url) as ws:
                print("✅ Connected to Iborain Safety Cloud Brain!")
                if hud:
                    hud.render_idle("ONLINE: SCANNING")

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
                            threat = data.get("threatLevel", "CLEARED")
                            msg = data.get("message", "")
                            fp = data.get("fingerprint", {})
                            plate = fp.get("plate", "UNPLATED") if fp else "UNPLATED"
                            v_type = fp.get("vehicleType", "VEHICLE") if fp else "VEHICLE"
                            latency = data.get("latencyMs", 310)

                            print(f"🚨 Sentry Alert -> Threat: [{threat}] | Plate: {plate} | Status: {msg}")
                            if fp:
                                print(f"   📋 Transit Forensic Record: Plate={plate} | Type={v_type} | Traits={fp.get('traits')}")

                            # Update the 1.28" TFT LCD HUD in real time!
                            if hud:
                                hud.render_result(plate=plate, vehicle_type=v_type, threat=threat, latency_ms=latency)

                        elif msg_type == "interrupted":
                            print("⚡ Scene reset -> Returning to idle scan")
                            if hud:
                                hud.render_idle("SCANNING...")
                        elif msg_type == "bye":
                            print(f"🚪 Session closed by server ({data.get('reason')})")
                            break
                    elif isinstance(message, bytes):
                        # Binary frame: [1B type][8B timestamp][payload]
                        if len(message) >= 9:
                            frame_type = message[0]
                            if frame_type == 0x02: # JPEG Vision Diff Ack
                                print(f"📷 Vision frame processed: {len(message)} bytes")
        except Exception as e:
            print(f"⚠️ Sentry connection dropped: {e}. Reconnecting in 3s...")
            if hud:
                hud.render_idle("RECONNECTING...")
            await asyncio.sleep(3)

if __name__ == "__main__":
    try:
        asyncio.run(run_sentry())
    except KeyboardInterrupt:
        if hud:
            hud.render_idle("STANDBY")
        print("\nSentry deactivated.")
