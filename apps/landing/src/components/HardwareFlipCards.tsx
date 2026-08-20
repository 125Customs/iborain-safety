"use client";

import React, { useState } from "react";
import { Cpu, Sun, ShieldCheck, Radio, RotateCw } from "lucide-react";

interface HardwareCardProps {
  name: string;
  category: string;
  specs: string[];
  studioTitle: string;
  studioDesc: string;
  mountedTitle: string;
  mountedDesc: string;
  telemetryMetric: string;
  icon: React.ElementType;
}

function FlipCard({ item }: { item: HardwareCardProps }) {
  const [isFlipped, setIsFlipped] = useState(false);
  const Icon = item.icon;

  return (
    <div
      className="perspective-1000 h-[460px] w-full cursor-pointer group"
      onMouseEnter={() => setIsFlipped(true)}
      onMouseLeave={() => setIsFlipped(false)}
      onClick={() => setIsFlipped(!isFlipped)}
    >
      <div
        className={`relative w-full h-full duration-700 transform-style-3d transition-transform ease-out ${
          isFlipped ? "rotate-y-180" : ""
        }`}
      >
        {/* FRONT: Clean Studio Cutout */}
        <div className="absolute inset-0 w-full h-full backface-hidden rounded-3xl glass-panel border border-emerald-500/20 p-7 flex flex-col justify-between shadow-xl bg-[#08150d]/90">
          <div>
            <div className="flex items-center justify-between gap-2 mb-6">
              <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
                <Icon className="w-5 h-5" />
              </div>
              <span className="text-[10px] font-mono uppercase tracking-widest text-emerald-400/80 px-2.5 py-1 rounded-full bg-emerald-950/60 border border-emerald-500/20 flex items-center gap-1.5">
                <RotateCw className="w-3 h-3 animate-spin" />
                Hover to Flip
              </span>
            </div>

            <span className="text-xs font-mono uppercase tracking-widest text-emerald-400 font-semibold block mb-1">
              {item.category}
            </span>
            <h3 className="text-2xl font-bold text-white tracking-tight mb-3">
              {item.name}
            </h3>
            <p className="text-xs sm:text-sm text-neutral-300 font-light leading-relaxed mb-6">
              {item.studioDesc}
            </p>
          </div>

          <div>
            <div className="space-y-2 mb-6 pt-4 border-t border-emerald-500/15">
              {item.specs.map((spec, idx) => (
                <div key={idx} className="flex items-center gap-2 text-xs font-mono text-neutral-300">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                  <span>{spec}</span>
                </div>
              ))}
            </div>

            <div className="flex items-center justify-between text-xs font-mono text-emerald-400 pt-3 border-t border-emerald-500/10">
              <span>{item.studioTitle}</span>
              <span className="text-white font-bold">{item.telemetryMetric}</span>
            </div>
          </div>
        </div>

        {/* BACK: Mounted Street-Pole Installation */}
        <div className="absolute inset-0 w-full h-full backface-hidden rotate-y-180 rounded-3xl glass-panel border border-emerald-400/35 p-7 flex flex-col justify-between shadow-2xl bg-[#040e07] text-white">
          <div>
            <div className="flex items-center justify-between gap-2 mb-6">
              <span className="text-[10px] font-mono uppercase tracking-widest text-black bg-emerald-400 px-3 py-1 rounded-full font-bold">
                Field Deployment View
              </span>
              <span className="text-xs font-mono text-emerald-300">Pole Mounted</span>
            </div>

            <h3 className="text-xl font-bold text-emerald-300 tracking-tight mb-2">
              {item.mountedTitle}
            </h3>
            <p className="text-xs sm:text-sm text-neutral-200 font-light leading-relaxed mb-6">
              {item.mountedDesc}
            </p>

            {/* Field Telemetry Radar Frame */}
            <div className="p-4 rounded-xl bg-[#020704] border border-emerald-500/20 font-mono text-xs space-y-2.5">
              <div className="flex items-center justify-between text-neutral-400 text-[11px] pb-2 border-b border-emerald-500/10">
                <span>MOUNTING STANDARD</span>
                <span className="text-emerald-400 font-bold">Universal Band-it 3/4&quot;</span>
              </div>
              <div className="flex items-center justify-between text-neutral-400 text-[11px] pb-2 border-b border-emerald-500/10">
                <span>WEATHER RESISTANCE</span>
                <span className="text-emerald-400 font-bold">IP67 Tropical Heavy Rain</span>
              </div>
              <div className="flex items-center justify-between text-neutral-400 text-[11px]">
                <span>ANTI-TAMPER LOCK</span>
                <span className="text-emerald-400 font-bold">MPU-6500 Active</span>
              </div>
            </div>
          </div>

          <div className="pt-4 border-t border-emerald-500/20 flex items-center justify-between text-xs font-mono text-neutral-400">
            <span>Fast 15-Minute Install</span>
            <span className="text-emerald-300 font-semibold">Ready for Deployment</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export function HardwareFlipCards() {
  const hardwareList: HardwareCardProps[] = [
    {
      name: "Sentry Core Node",
      category: "Edge Neural Unit",
      icon: Cpu,
      studioTitle: "Optical Resolution",
      telemetryMetric: "Sony IMX500 12.3MP",
      studioDesc:
        "Streamlined vision sentry unit engineered with on-sensor neural DSP and Raspberry Pi Zero 2 for sub-30ms vehicle classification.",
      specs: [
        "Sony IMX500 Neural Vision Sensor",
        "Raspberry Pi Zero 2 W Co-Processor",
        "Quad-Band 4G LTE-M / IoT SIM Uplink",
      ],
      mountedTitle: "Arterial Street Pole Installation",
      mountedDesc:
        "Mounted at 2.4m–4.5m height on utility poles or gateposts. Delivers sharp optical coverage across dual-lane transit corridors with zero blind spots.",
    },
    {
      name: "Solar Canopy Kit",
      category: "Power Autonomy",
      icon: Sun,
      studioTitle: "Power Reserve",
      telemetryMetric: "72-Hour Rainy Buffer",
      studioDesc:
        "Cord-free monocrystalline solar roof paired with a temperature-resilient LiFePO4 battery pack and intelligent MPPT power controller.",
      specs: [
        "30W Monocrystalline PV Surface",
        "12.8V LiFePO4 Solid-State Battery",
        "Zero Trenching or Grid Cabling",
      ],
      mountedTitle: "Overhead Canopy Deployment",
      mountedDesc:
        "Engineered with anti-soiling hydrophobic coating to resist African road dust. Harvests full operational charge with only 3.2 peak sunlight hours.",
    },
    {
      name: "Anti-Theft & Stealth Core",
      category: "Hardware Integrity",
      icon: ShieldCheck,
      studioTitle: "Vibration Detection",
      telemetryMetric: "6-Axis MPU-6500 IMU",
      studioDesc:
        "100% silent stealth operation in a sealed matte-black enclosure with continuous 6-axis inertial motion tracking to prevent theft or tampering.",
      specs: [
        "MPU-6500 6-Axis Motion/Tilt IMU",
        "100% Stealth Matte-Black Casing",
        "Instant WhatsApp Theft Dispatch",
      ],
      mountedTitle: "Active Anti-Tamper Protection",
      mountedDesc:
        "Detects pole impacts, physical vibration, or unauthorized removal attempts, triggering instant encrypted alerts to neighborhood patrols.",
    },
    {
      name: "FreeForm™ Mesh Gateway",
      category: "Corridor Coordinator",
      icon: Radio,
      studioTitle: "Mesh Propagation",
      telemetryMetric: "<400ms Hotlist Sync",
      studioDesc:
        "Decentralized edge coordinator maintaining continuous cellular sync and synchronized vector memory bank for inter-community grids.",
      specs: [
        "Dual-SIM 4G LTE Cellular Modem",
        "Encrypted SQLite Vector Hotlist Cache",
        "Automated WhatsApp Dispatch Bridge",
      ],
      mountedTitle: "Inter-Estate Control Point",
      mountedDesc:
        "Bridges isolated estate perimeters into a unified regional safety ring. Relays real-time vehicle vectors directly into patrol responder channels.",
    },
  ];

  return (
    <section id="hardware" className="relative py-28 md:py-40 px-4 bg-[#060b08]">
      <div className="max-w-6xl mx-auto">
        
        {/* Section Header */}
        <div className="flex flex-col items-center text-center mb-16 md:mb-24">
          <span className="text-xs font-mono uppercase tracking-widest text-emerald-400 font-semibold mb-3">
            Physical Hardware Architecture
          </span>
          <h2 className="text-3xl sm:text-5xl font-bold text-white tracking-tight max-w-3xl">
            Engineered for African Roads. Zero Trenching. Zero Grid Power.
          </h2>
          <p className="mt-4 text-base sm:text-lg text-neutral-400 max-w-2xl font-light">
            Every Iborain hardware node is 100% cord-free and clamps to existing utility poles in 15 minutes.
            Hover over any hardware unit to inspect its physical street-pole deployment.
          </p>
        </div>

        {/* 3D Flip Card Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {hardwareList.map((item, idx) => (
            <FlipCard key={idx} item={item} />
          ))}
        </div>

      </div>
    </section>
  );
}
