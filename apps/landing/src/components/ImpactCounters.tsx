"use client";

import React from "react";
import { Activity, ShieldAlert, Zap, Clock } from "lucide-react";

export function ImpactCounters() {
  const stats = [
    {
      value: "45,000+",
      label: "Transit Movements Fingerprinted",
      subtext: "Daily multimodal edge evaluations across active Nairobi corridors.",
      icon: Activity,
    },
    {
      value: "89%",
      label: "Localized Crime Reduction",
      subtext: "Verified drop in transit theft and perimeter intrusions in deployed sectors.",
      icon: ShieldAlert,
    },
    {
      value: "<3 Min",
      label: "Patrol Response Latency",
      subtext: "From neural sentry detection to physical ground guard dispatch.",
      icon: Clock,
    },
    {
      value: "<400ms",
      label: "10km Regional Mesh Sync",
      subtext: "Decentralized cryptographic hotlist distribution between estates.",
      icon: Zap,
    },
  ];

  return (
    <section className="relative py-24 md:py-36 px-4 bg-[#060b08] border-t border-emerald-500/10">
      <div className="max-w-6xl mx-auto">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {stats.map((stat, idx) => {
            const Icon = stat.icon;
            return (
              <div
                key={idx}
                className="p-7 rounded-3xl glass-panel border border-emerald-500/15 hover:border-emerald-500/35 transition-all duration-300 flex flex-col justify-between group"
              >
                <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 mb-6 group-hover:scale-110 transition-transform">
                  <Icon className="w-5 h-5" />
                </div>
                <div>
                  <div className="text-4xl sm:text-5xl font-black text-transparent bg-clip-text bg-gradient-to-br from-white via-neutral-100 to-emerald-400 tracking-tight font-mono mb-2">
                    {stat.value}
                  </div>
                  <h3 className="text-sm font-semibold text-white tracking-tight mb-2">
                    {stat.label}
                  </h3>
                  <p className="text-xs text-neutral-400 font-light leading-relaxed">
                    {stat.subtext}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
