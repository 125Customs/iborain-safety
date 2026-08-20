#!/usr/bin/env python3
"""
Iborain Safety - Edge Sentry Tactical Terminal & LCD HUD Simulator.
Produces timed, hyper-realistic, colorized edge logs and synchronized GC9A01 LCD screen output
for video demos, pitch presentations, and developer previews.
"""
import os
import sys
import time
import random
import argparse
from datetime import datetime

# Attempt to load the physical GC9A01 Round TFT Display driver
try:
    from display import SentryDisplay
    hud = SentryDisplay(enabled=True)
except Exception:
    hud = None

# ANSI Terminal Colors
GREEN = "\033[92m"
BLUE = "\033[94m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

def ts():
    return f"{DIM}[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}]{RESET}"

def log(msg, delay=0.0, speed=1.0):
    print(f"{ts()} {msg}", flush=True)
    if delay > 0:
        time.sleep(delay / speed)

SCENARIOS = [
    {
        "id": "resident_clearance",
        "trigger": "Motion Vector in Gate ROI (Confidence: 0.985)",
        "plate": "KDE 842X",
        "type": "White Toyota Land Cruiser Prado (2021)",
        "traits": "Tinted windows, roof rack, front bull-bar",
        "threat": "CLEARED: RESIDENT_AUTH",
        "resident": "Unit #402 (Dr. Kamau - Court Security Chair)",
        "latency_ms": 142,
        "is_threat": False,
        "hud_status": "CLEARED"
    },
    {
        "id": "delivery_clearance",
        "trigger": "Optical Trigger Zone B (Gatehouse Approach Lane 1)",
        "plate": "KBY 120Z",
        "type": "Silver Isuzu D-Max Double Cabin",
        "traits": "Commercial canopy, rear gate clearance sticker #12",
        "threat": "CLEARED: DELIVERY_REGISTERED",
        "resident": "DHL Express Courier (Waybill #9921-KE)",
        "latency_ms": 168,
        "is_threat": False,
        "hud_status": "CLEARED"
    },
    {
        "id": "hotlist_stolen_intercept",
        "trigger": "High-Velocity Vehicle Ingress (34 km/h approaching barrier)",
        "plate": "KDF 441A",
        "type": "Black Subaru Forester XT",
        "traits": "Unregistered visitor, rapid approach, missing front inspection decal",
        "threat": "🚨 HOTLIST_ALERT: STOLEN_VEHICLE_APB #2026-901",
        "resident": "UNAUTHORIZED - IMMEDIATE SECURITY INTERCEPT",
        "latency_ms": 129,
        "is_threat": True,
        "hud_status": "HOTLIST MATCH"
    }
]

def run_init_sequence(speed=1.0):
    print(f"\n{BOLD}{CYAN}======================================================================{RESET}")
    print(f"{BOLD}{GREEN}  🛡️  IBORAIN SAFETY AI EDGE SENTRY - OS v2.4.1 (STEALTH BUILD){RESET}")
    print(f"{BOLD}{CYAN}======================================================================{RESET}\n")
    time.sleep(0.4 / speed)

    if hud:
        hud.render_idle("INITIALIZING...")

    log(f"{BLUE}⚙️  [SYS_INIT]{RESET} Initializing Edge Sentry node: {BOLD}sentry-nairobi-gate-01{RESET}", 0.25, speed)
    log(f"{BLUE}⚙️  [HW_CHECK]{RESET} Testing I2C bus: MPU-6500 Anti-Tamper 6-Axis IMU ... {GREEN}ONLINE (0x68){RESET}", 0.3, speed)
    log(f"{BLUE}⚙️  [HW_CHECK]{RESET} Probing Sony IMX500 AI Camera DSP (CSI-2 2-Lane) ... {GREEN}LOCKED (1080p @ 30fps){RESET}", 0.35, speed)
    
    if hud and getattr(hud, 'enabled', False):
        log(f"{BLUE}⚙️  [HW_CHECK]{RESET} GC9A01 TFT Diagnostic Round HUD (SPI 40MHz) ... {GREEN}ACTIVE{RESET}", 0.25, speed)
    else:
        log(f"{BLUE}⚙️  [HW_CHECK]{RESET} GC9A01 Diagnostic Screen ... {DIM}STEALTH MODE (HEADLESS){RESET}", 0.25, speed)

    log(f"{BLUE}🌐 [NETWORK]{RESET} Cellular 4G LTE link established (18.4 Mbps, -62 dBm RSSI)", 0.3, speed)
    log(f"{BLUE}🔒 [CRYPTO]{RESET} Edge TLS 1.3 session negotiated with wss://edge.iborain.cloud", 0.3, speed)
    log(f"{GREEN}✅ [STATE]{RESET} Sentry authenticated (Session: {BOLD}sess_9a8f21b7{RESET}) -> {GREEN}ARMED & SCANNING{RESET}\n", 0.8, speed)

    if hud:
        hud.render_idle("ONLINE: SCANNING")

def execute_scenario(s, speed=1.0):
    # 1. Idle optical scanning diffs
    for _ in range(random.randint(2, 3)):
        fps = random.randint(29, 30)
        diff = random.randint(14, 42)
        log(f"{DIM}👁️  [DSP_IDLE] Optical stream stable | 1080p@{fps}fps | Diff: {diff} B | Shutter: 1/400s{RESET}", 0.3, speed)

    print()
    log(f"{YELLOW}⚡ [TRIGGER]{RESET} {BOLD}{s['trigger']}{RESET}", 0.15, speed)
    log(f"{CYAN}📷 [VISION]{RESET} Captured high-res ROI frame (14.2 KB) -> Dispatching to Gemini Live...", 0.15, speed)
    log(f"{CYAN}🧠 [MULTIMODAL]{RESET} Streaming latent tokens to Cloud Run Gemini Brain...", 0.25, speed)

    # Update physical HUD if available
    if hud:
        hud.render_result(
            plate=s["plate"],
            vehicle_type=s["type"].split("(")[0].strip(),
            threat=s["hud_status"],
            latency_ms=s["latency_ms"]
        )

    # Threat vs Cleared Output
    if s["is_threat"]:
        log(f"{RED}{BOLD}🚨 [THREAT DETECTED]{RESET} {RED}{s['threat']}{RESET}", 0.1, speed)
        log(f"   {RED}├─ Plate:{RESET} {BOLD}{s['plate']}{RESET} | {RED}Confidence:{RESET} 99.4%")
        log(f"   {RED}├─ Vehicle:{RESET} {s['type']}")
        log(f"   {RED}├─ Traits:{RESET} {s['traits']}")
        log(f"   {RED}├─ Status:{RESET} {BOLD}{s['resident']}{RESET}")
        log(f"   {RED}└─ Latency:{RESET} {GREEN}{s['latency_ms']}ms{RESET} (Edge-to-Inference) | Cost: $0.0014")
        log(f"{RED}📲 [DISPATCH]{RESET} Automated WhatsApp Alert sent to Estate Security Group + Head Guard", 0.25, speed)
        log(f"{RED}🔊 [AUDIO]{RESET} Synthesized Gate Siren & Guard Intercom Directive triggered", 0.35, speed)
    else:
        log(f"{GREEN}{BOLD}✨ [VERDICT]{RESET} {GREEN}{s['threat']}{RESET}", 0.1, speed)
        log(f"   {GREEN}├─ Plate:{RESET} {BOLD}{s['plate']}{RESET} | {GREEN}Confidence:{RESET} 98.9%")
        log(f"   {GREEN}├─ Vehicle:{RESET} {s['type']}")
        log(f"   {GREEN}├─ Match:{RESET} {s['resident']}")
        log(f"   {GREEN}└─ Latency:{RESET} {GREEN}{s['latency_ms']}ms{RESET} | Cost: $0.0014")
        log(f"{BLUE}📲 [WHATSAPP]{RESET} Resident arrival notification pushed to {s['resident'].split(' ')[0]}", 0.25, speed)
        log(f"{GREEN}🟢 [BARRIER]{RESET} Relay pulse -> Gate barrier auto-cleared (Hold 8s)", 0.35, speed)

    print()
    time.sleep(1.8 / speed)

    # Return to scanning
    if hud:
        hud.render_idle("SCANNING...")

def execute_tamper_demo(speed=1.0):
    log(f"{YELLOW}⚠️  [IMU_INTERRUPT] 6-Axis Accelerometer Shock Spike (ΔG = 2.85g on Z-axis, Tilt: 22°){RESET}", 0.2, speed)
    log(f"{RED}{BOLD}🚨 [TAMPER ALERT]{RESET} Enclosure vibration/tilt threshold exceeded! GPS coords locked.", 0.2, speed)
    if hud:
        hud.render_tamper()
    log(f"{RED}📲 [DISPATCH]{RESET} High-priority SMS & WhatsApp sent to Admin: 'SENTRY_01_TAMPER_DETECTED'", 0.4, speed)
    log(f"{RED}📍 [TELEMETRY]{RESET} Cellular Cell-Tower Triangulation logged -> Incident DB #8812", 0.3, speed)
    time.sleep(2.0 / speed)
    log(f"{GREEN}🔄 [RESET]{RESET} Scene stabilized -> Restoring baseline calibration.\n", 0.6, speed)
    if hud:
        hud.render_idle("ONLINE: SCANNING")

def main():
    parser = argparse.ArgumentParser(description="Iborain Safety Edge Sentry Demo Log & Screen Simulator")
    parser.add_argument("--demo", "-d", action="store_true", help="Run in demo mode")
    parser.add_argument("--speed", type=float, default=1.0, help="Playback speed multiplier (e.g. 1.5 for faster, 0.8 for slower)")
    parser.add_argument("--loop", action="store_true", help="Run indefinitely in a loop for continuous video takes")
    parser.add_argument("--scenario", type=str, choices=["resident", "delivery", "stolen", "tamper", "all"], default="all", help="Select a specific scenario to demo")
    args = parser.parse_args()

    run_init_sequence(speed=args.speed)

    iteration = 1
    while True:
        if args.scenario == "resident":
            execute_scenario(SCENARIOS[0], speed=args.speed)
        elif args.scenario == "delivery":
            execute_scenario(SCENARIOS[1], speed=args.speed)
        elif args.scenario == "stolen":
            execute_scenario(SCENARIOS[2], speed=args.speed)
        elif args.scenario == "tamper":
            execute_tamper_demo(speed=args.speed)
        else: # all
            for s in SCENARIOS:
                execute_scenario(s, speed=args.speed)
            execute_tamper_demo(speed=args.speed)

        if not args.loop:
            break
        
        iteration += 1
        log(f"{DIM}--- [CYCLE {iteration} COMPLETE] Pausing for next ingress event ---{RESET}\n", 1.5, args.speed)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        if hud:
            hud.render_idle("STANDBY")
        print(f"\n{YELLOW}Demo simulation terminated by user.{RESET}")
