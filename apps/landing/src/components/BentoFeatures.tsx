"use client";

import React, { useState } from "react";
import { Eye, ShieldAlert, Cpu, Radio, Sun, Volume2, Search, Check, Sparkles } from "lucide-react";

export function BentoFeatures() {
  const [activeReasoningTab, setActiveReasoningTab] = useState<"probox" | "boda" | "cargo">("probox");

  return (
    <section id="features" className="relative py-28 md:py-40 px-4 bg-[#060b08]">
      <div className="max-w-6xl mx-auto">
        
        {/* Section Header */}
        <div className="flex flex-col items-center text-center mb-16 md:mb-24">
          <span className="text-xs font-mono uppercase tracking-widest text-emerald-400 font-semibold mb-3">
            Neural Vision & Edge Architecture
          </span>
          <h2 className="text-3xl sm:text-5xl font-bold text-white tracking-tight max-w-3xl">
            Beyond License Plate OCR. Real-Time Multimodal Transit Reasoning.
          </h2>
          <p className="mt-4 text-base sm:text-lg text-neutral-400 max-w-2xl font-light">
            Standard automated number plate cameras fail on Kenyan roads. Iborain fuses on-sensor Sony IMX500
            diff vectors with Google Gemini 3.7 Flash to reason over physical modifications, cargo, and rider gear.
          </p>
        </div>

        {/* Gapless Bento Grid with grid-flow-dense */}
        <div className="grid grid-cols-12 gap-6 grid-flow-dense">
          
          {/* Card 1 (Large 8-col): Multimodal African Transit Forensics Engine */}
          <div className="col-span-12 lg:col-span-8 p-6 sm:p-8 rounded-3xl glass-panel border border-emerald-500/20 hover:border-emerald-500/40 transition-all duration-500 flex flex-col justify-between group overflow-hidden relative">
            <div className="absolute top-0 right-0 w-96 h-96 bg-emerald-500/5 rounded-full blur-3xl pointer-events-none" />

            <div>
              <div className="flex items-center justify-between gap-4 mb-6">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-xs font-mono text-emerald-400 font-medium">
                  <Cpu className="w-3.5 h-3.5 text-emerald-400" />
                  Sony IMX500 + Gemini 3.7 Flash
                </div>
                <span className="text-xs font-mono text-emerald-300/80 bg-[#07150c] px-2.5 py-1 rounded-md border border-emerald-500/15">
                  Vector Diff: 28ms
                </span>
              </div>

              <h3 className="text-2xl sm:text-3xl font-bold text-white tracking-tight mb-3">
                Multimodal African Transit Forensics
              </h3>
              <p className="text-sm text-neutral-300 leading-relaxed max-w-2xl font-light mb-6">
                When license plates are covered in wet clay, missing, or obscured by commercial cargo, Iborain
                evaluates vehicle geometry, roof racks, body dents, window tints, motorbike fuel tank colors, and anomalous payloads.
              </p>

              {/* Interactive Classifier Switcher */}
              <div className="flex flex-wrap gap-2 mb-6">
                <button
                  onClick={() => setActiveReasoningTab("probox")}
                  className={`px-3.5 py-1.5 rounded-lg text-xs font-mono transition-all cursor-pointer ${
                    activeReasoningTab === "probox"
                      ? "bg-emerald-500 text-black font-semibold shadow-md shadow-emerald-500/20"
                      : "bg-[#09140e] text-neutral-400 hover:text-white border border-emerald-500/15"
                  }`}
                >
                  Modified Probox Profile
                </button>
                <button
                  onClick={() => setActiveReasoningTab("boda")}
                  className={`px-3.5 py-1.5 rounded-lg text-xs font-mono transition-all cursor-pointer ${
                    activeReasoningTab === "boda"
                      ? "bg-emerald-500 text-black font-semibold shadow-md shadow-emerald-500/20"
                      : "bg-[#09140e] text-neutral-400 hover:text-white border border-emerald-500/15"
                  }`}
                >
                  Boda Boda Classification
                </button>
                <button
                  onClick={() => setActiveReasoningTab("cargo")}
                  className={`px-3.5 py-1.5 rounded-lg text-xs font-mono transition-all cursor-pointer ${
                    activeReasoningTab === "cargo"
                      ? "bg-emerald-500 text-black font-semibold shadow-md shadow-emerald-500/20"
                      : "bg-[#09140e] text-neutral-400 hover:text-white border border-emerald-500/15"
                  }`}
                >
                  Anomalous Cargo (13kg Gas)
                </button>
              </div>
            </div>

            {/* Visual Telemetry Box */}
            <div className="p-4 sm:p-5 rounded-2xl bg-[#050e08] border border-emerald-500/20 font-mono text-xs text-neutral-300">
              {activeReasoningTab === "probox" && (
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-emerald-400 text-[11px] pb-2 border-b border-emerald-500/10">
                    <span>DETECTION TARGET: VEHICLE_PROBOX_MODIFIED</span>
                    <span className="text-emerald-300 font-bold">CONFIDENCE: 98.7%</span>
                  </div>
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-1 text-[11px]">
                    <div className="p-2 rounded bg-[#09160f] border border-emerald-500/10">
                      <span className="text-neutral-400 block text-[10px]">Plate Condition</span>
                      <span className="text-amber-400 font-medium">Mud-Obscured (68%)</span>
                    </div>
                    <div className="p-2 rounded bg-[#09160f] border border-emerald-500/10">
                      <span className="text-neutral-400 block text-[10px]">Roof Rack</span>
                      <span className="text-emerald-300 font-medium">Commercial Welded</span>
                    </div>
                    <div className="p-2 rounded bg-[#09160f] border border-emerald-500/10">
                      <span className="text-neutral-400 block text-[10px]">Window Tint</span>
                      <span className="text-emerald-300 font-medium">Dark Limo 5%</span>
                    </div>
                    <div className="p-2 rounded bg-[#09160f] border border-emerald-500/10">
                      <span className="text-neutral-400 block text-[10px]">Body Marker</span>
                      <span className="text-emerald-300 font-medium">Left Quarter Dent</span>
                    </div>
                  </div>
                </div>
              )}

              {activeReasoningTab === "boda" && (
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-emerald-400 text-[11px] pb-2 border-b border-emerald-500/10">
                    <span>DETECTION TARGET: MOTORCYCLE_BODA_BODA</span>
                    <span className="text-emerald-300 font-bold">CONFIDENCE: 99.2%</span>
                  </div>
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-1 text-[11px]">
                    <div className="p-2 rounded bg-[#09160f] border border-emerald-500/10">
                      <span className="text-neutral-400 block text-[10px]">Model Series</span>
                      <span className="text-emerald-300 font-medium">Bajaj Boxer 150</span>
                    </div>
                    <div className="p-2 rounded bg-[#09160f] border border-emerald-500/10">
                      <span className="text-neutral-400 block text-[10px]">Fuel Tank Color</span>
                      <span className="text-emerald-300 font-medium">Crimson Red</span>
                    </div>
                    <div className="p-2 rounded bg-[#09160f] border border-emerald-500/10">
                      <span className="text-neutral-400 block text-[10px]">Rider Helmet</span>
                      <span className="text-emerald-400 font-medium">Yellow Reflector</span>
                    </div>
                    <div className="p-2 rounded bg-[#09160f] border border-emerald-500/10">
                      <span className="text-neutral-400 block text-[10px]">Passenger Count</span>
                      <span className="text-emerald-300 font-medium">1 Pillion Rider</span>
                    </div>
                  </div>
                </div>
              )}

              {activeReasoningTab === "cargo" && (
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-amber-400 text-[11px] pb-2 border-b border-amber-500/10">
                    <span>FLAGGED ANOMALY: COMMERCIAL_CARGO_RISK</span>
                    <span className="text-amber-300 font-bold">ALERT: DISPATCH_SYNC</span>
                  </div>
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-1 text-[11px]">
                    <div className="p-2 rounded bg-[#09160f] border border-emerald-500/10">
                      <span className="text-neutral-400 block text-[10px]">Cargo Classification</span>
                      <span className="text-amber-400 font-medium">13kg LPG Gas Cylinder</span>
                    </div>
                    <div className="p-2 rounded bg-[#09160f] border border-emerald-500/10">
                      <span className="text-neutral-400 block text-[10px]">Transit Mode</span>
                      <span className="text-neutral-200 font-medium">Rear Rack Strap</span>
                    </div>
                    <div className="p-2 rounded bg-[#09160f] border border-emerald-500/10">
                      <span className="text-neutral-400 block text-[10px]">Corridor Time</span>
                      <span className="text-neutral-200 font-medium">02:14 AM (Off-Hour)</span>
                    </div>
                    <div className="p-2 rounded bg-[#09160f] border border-emerald-500/10">
                      <span className="text-neutral-400 block text-[10px]">Auto WhatsApp Alert</span>
                      <span className="text-emerald-400 font-medium">Dispatched to SACCO</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Card 2 (4-col): Sub-400ms 10km Decentralized Threat Mesh */}
          <div className="col-span-12 lg:col-span-4 p-6 sm:p-8 rounded-3xl glass-panel border border-emerald-500/20 hover:border-emerald-500/40 transition-all duration-500 flex flex-col justify-between group">
            <div>
              <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 mb-6 group-hover:scale-110 transition-transform">
                <Radio className="w-5 h-5 text-emerald-400" />
              </div>
              <h3 className="text-xl sm:text-2xl font-bold text-white tracking-tight mb-2">
                10km Threat Mesh
              </h3>
              <p className="text-xs sm:text-sm text-neutral-300 font-light leading-relaxed mb-6">
                When an estate perimeter or transit corridor sentry identifies a flagged hotlist vehicle,
                it broadcasts cryptographic vector tokens to all neighboring nodes within 10km in under 400ms without relying on cloud queues.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-[#050e08] border border-emerald-500/15 font-mono text-xs">
              <div className="flex items-center justify-between text-neutral-400 mb-2 pb-2 border-b border-emerald-500/10 text-[11px]">
                <span>MESH LATENCY</span>
                <span className="text-emerald-400 font-bold">&lt; 380 ms</span>
              </div>
              <div className="flex items-center justify-between text-neutral-400 text-[11px]">
                <span>HOTLIST SYNC RANGE</span>
                <span className="text-emerald-400 font-bold">10 km Radius</span>
              </div>
            </div>
          </div>

          {/* Card 3 (4-col): Edge-Level Active Deterrence */}
          <div className="col-span-12 lg:col-span-4 p-6 sm:p-8 rounded-3xl glass-panel border border-emerald-500/20 hover:border-emerald-500/40 transition-all duration-500 flex flex-col justify-between group">
            <div>
              <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 mb-6 group-hover:scale-110 transition-transform">
                <Volume2 className="w-5 h-5 text-emerald-400" />
              </div>
              <h3 className="text-xl sm:text-2xl font-bold text-white tracking-tight mb-2">
                Edge Active Deterrence
              </h3>
              <p className="text-xs sm:text-sm text-neutral-300 font-light leading-relaxed mb-6">
                Integrated GC9A01 ultra-bright radar strobes and MAX98357A 3W directional verbal horns
                actively warn unauthorized entries and hotlisted vehicles at the point of arrival.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-[#050e08] border border-emerald-500/15 font-mono text-xs space-y-2">
              <div className="flex items-center gap-2 text-[11px] text-emerald-300">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
                <span>GC9A01 Threat Strobe: 120Hz Flash</span>
              </div>
              <div className="flex items-center gap-2 text-[11px] text-neutral-400">
                <span className="w-2 h-2 rounded-full bg-emerald-500" />
                <span>3W Verbal Audio: Swahili / English</span>
              </div>
            </div>
          </div>

          {/* Card 4 (8-col): Anti-Theft MPU-6500 Clamp & Cord-Free Solar */}
          <div className="col-span-12 lg:col-span-8 p-6 sm:p-8 rounded-3xl glass-panel border border-emerald-500/20 hover:border-emerald-500/40 transition-all duration-500 flex flex-col justify-between group">
            <div>
              <div className="flex items-center justify-between gap-4 mb-6">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-xs font-mono text-emerald-400 font-medium">
                  <Sun className="w-3.5 h-3.5 text-emerald-400" />
                  Cord-Free Zero-CapEx Architecture
                </div>
                <span className="text-xs font-mono text-emerald-300/80 bg-[#07150c] px-2.5 py-1 rounded-md border border-emerald-500/15">
                  48-Hour Rainy Buffer
                </span>
              </div>

              <h3 className="text-2xl sm:text-3xl font-bold text-white tracking-tight mb-3">
                Solar-Ready Canopy & Anti-Theft Gyro Clamp
              </h3>
              <p className="text-sm text-neutral-300 leading-relaxed max-w-2xl font-light mb-6">
                Each node is powered by an overhead monocrystalline solar canopy with smart MPPT power management.
                Protected by an internal MPU-6500 6-axis gyroscope clamp that instantly triggers acoustic alarms and GPS tamper distress
                if an unauthorized individual attempts pole removal.
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2">
              <div className="p-4 rounded-xl bg-[#050e08] border border-emerald-500/15">
                <span className="text-xs font-mono text-neutral-400 block mb-1">Power Autonomy</span>
                <span className="text-lg font-bold text-white">100% Cord-Free</span>
                <p className="text-[11px] text-neutral-400 mt-1">48hr battery reserve for rainy seasons</p>
              </div>
              <div className="p-4 rounded-xl bg-[#050e08] border border-emerald-500/15">
                <span className="text-xs font-mono text-neutral-400 block mb-1">Anti-Theft Protection</span>
                <span className="text-lg font-bold text-white">MPU-6500 Clamp</span>
                <p className="text-[11px] text-neutral-400 mt-1">6-axis vibration & tilt lock sensor</p>
              </div>
              <div className="p-4 rounded-xl bg-[#050e08] border border-emerald-500/15">
                <span className="text-xs font-mono text-neutral-400 block mb-1">Deployment Speed</span>
                <span className="text-lg font-bold text-white">15 Minutes</span>
                <p className="text-[11px] text-neutral-400 mt-1">Band-it clamp on standard street poles</p>
              </div>
            </div>

          </div>

        </div>

      </div>
    </section>
  );
}
