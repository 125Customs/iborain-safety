"use client";

import React from "react";
import { Shield, Sparkles, ArrowRight, Terminal, Zap, Radio, CheckCircle2 } from "lucide-react";

export function Hero() {
  const scrollTo = (id: string) => {
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <section className="relative min-h-[90vh] flex flex-col justify-center items-center pt-36 pb-24 md:pt-48 md:pb-36 px-4 overflow-hidden radar-grid-bg">
      {/* Ambient Forest & Radar Glows */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[400px] bg-emerald-500/10 rounded-full blur-[140px] pointer-events-none" />
      <div className="absolute top-1/3 left-1/4 w-[350px] h-[350px] bg-teal-500/8 rounded-full blur-[100px] pointer-events-none" />
      <div className="absolute top-1/2 right-1/4 w-[400px] h-[400px] bg-emerald-900/15 rounded-full blur-[120px] pointer-events-none" />

      {/* Main Container */}
      <div className="relative z-10 w-full max-w-6xl mx-auto flex flex-col items-center text-center">
        
        {/* Status Chip */}
        <div className="inline-flex items-center gap-2.5 px-4 py-1.5 rounded-full glass-panel border border-emerald-500/25 mb-8 shadow-inner">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500" />
          </span>
          <span className="text-xs font-mono tracking-wider text-emerald-300 uppercase">
            Solar-Ready Edge AI Sentry Grid
          </span>
          <span className="text-xs text-neutral-500 font-mono">|</span>
          <span className="text-xs font-mono text-neutral-400">Kenya ODPC Compliant</span>
        </div>

        {/* 2-Line Iron Rule Headline with Inline Typography Visual Accent */}
        <h1 className="text-4xl sm:text-6xl lg:text-7xl font-bold tracking-tight text-white max-w-6xl mx-auto leading-[1.08]">
          Autonomous Edge AI Sentry Grid{" "}
          <span className="inline-flex items-center align-middle mx-1.5 px-3 py-1 rounded-full bg-emerald-950/60 border border-emerald-500/30 text-emerald-400 text-2xl sm:text-4xl font-mono tracking-normal">
            <Radio className="w-5 h-5 sm:w-8 sm:h-8 inline-block animate-pulse text-emerald-400 mr-2" />
            10km Mesh
          </span>{" "}
          for African Transit Corridors
        </h1>

        {/* Editorial Subtitle */}
        <p className="mt-8 text-base sm:text-xl text-neutral-300 max-w-3xl mx-auto font-light leading-relaxed">
          Deploy low-cost, pole-mounted sentry hardware across estates, SACCO corridors, and logistics hubs.
          Powered by onboard Sony IMX500 neural vision and Gemini 3.7 Flash to fingerprint unplated vehicles,
          Boda Boda cargo, and dispatch automated WhatsApp patrol alerts in under 400 milliseconds.
        </p>

        {/* High-Contrast Dual Action CTAs */}
        <div className="mt-10 flex flex-col sm:flex-row items-center gap-4 w-full justify-center">
          <button
            onClick={() => scrollTo("pricing")}
            className="w-full sm:w-auto px-8 py-4 rounded-full text-sm font-semibold text-black bg-emerald-400 hover:bg-emerald-300 transition-all duration-300 shadow-xl shadow-emerald-500/25 flex items-center justify-center gap-3 group cursor-pointer active:scale-95"
          >
            <span>Pre-Order Sentry Nodes ($49/mo)</span>
            <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
          </button>

          <button
            onClick={() => scrollTo("terminal")}
            className="w-full sm:w-auto px-8 py-4 rounded-full text-sm font-medium text-neutral-200 glass-panel hover:bg-emerald-950/40 hover:border-emerald-500/40 transition-all duration-300 flex items-center justify-center gap-2.5 cursor-pointer active:scale-95"
          >
            <Terminal className="w-4 h-4 text-emerald-400" />
            <span>Launch FreeForm™ Crime Search</span>
          </button>
        </div>

        {/* Floating Telemetry Stream Pills */}
        <div className="mt-16 w-full max-w-5xl grid grid-cols-1 md:grid-cols-3 gap-4 text-left">
          
          {/* Telemetry Card 1 */}
          <div className="p-4 rounded-2xl glass-panel border border-emerald-500/15 hover:border-emerald-500/35 transition-all duration-300 flex items-start gap-3.5">
            <div className="w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center shrink-0 mt-0.5">
              <Zap className="w-4 h-4 text-emerald-400" />
            </div>
            <div>
              <div className="flex items-center justify-between gap-2">
                <span className="text-[11px] font-mono uppercase tracking-wider text-emerald-400 font-semibold">
                  Mombasa Road Node #04
                </span>
                <span className="text-[10px] font-mono text-neutral-400">12s ago</span>
              </div>
              <p className="text-xs text-neutral-300 mt-1 leading-snug">
                Mud-obscured plate resolved via rear roof rack geometry & commercial cargo profile.
              </p>
            </div>
          </div>

          {/* Telemetry Card 2 */}
          <div className="p-4 rounded-2xl glass-panel border border-emerald-500/15 hover:border-emerald-500/35 transition-all duration-300 flex items-start gap-3.5">
            <div className="w-8 h-8 rounded-lg bg-amber-500/10 border border-amber-500/20 flex items-center justify-center shrink-0 mt-0.5">
              <Shield className="w-4 h-4 text-amber-400" />
            </div>
            <div>
              <div className="flex items-center justify-between gap-2">
                <span className="text-[11px] font-mono uppercase tracking-wider text-amber-400 font-semibold">
                  Eastleigh Commercial Hub
                </span>
                <span className="text-[10px] font-mono text-neutral-400">45s ago</span>
              </div>
              <p className="text-xs text-neutral-300 mt-1 leading-snug">
                Unregistered Boxer 150 + anomalous 13kg gas cylinder payload flagged for patrol.
              </p>
            </div>
          </div>

          {/* Telemetry Card 3 */}
          <div className="p-4 rounded-2xl glass-panel border border-emerald-500/15 hover:border-emerald-500/35 transition-all duration-300 flex items-start gap-3.5">
            <div className="w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center shrink-0 mt-0.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            </div>
            <div>
              <div className="flex items-center justify-between gap-2">
                <span className="text-[11px] font-mono uppercase tracking-wider text-emerald-400 font-semibold">
                  10km Hotlist Mesh Sync
                </span>
                <span className="text-[10px] font-mono text-emerald-300 font-bold">312ms</span>
              </div>
              <p className="text-xs text-neutral-300 mt-1 leading-snug">
                14 perimeter nodes synchronized across Syokimau corridor with zero cellular lag.
              </p>
            </div>
          </div>

        </div>

      </div>
    </section>
  );
}
