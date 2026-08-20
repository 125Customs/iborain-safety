"use client";

import React from "react";
import { Shield, Cpu, Bus, Building2, Radio } from "lucide-react";

export function PartnersMarquee() {
  const partners = [
    { name: "Forward Travelers SACCO", type: "Transit Corridor", icon: Bus },
    { name: "Syokimau Estate Association", type: "Gated Community", icon: Building2 },
    { name: "Sony IMX500 Neural Vision", type: "Sensor Partner", icon: Cpu },
    { name: "2NK SACCO Transport Grid", type: "Arterial Fleet", icon: Bus },
    { name: "Karen Community Association", type: "Perimeter Mesh", icon: Shield },
    { name: "Google Cloud Run & Gemini", type: "AI Infrastructure", icon: Radio },
    { name: "Kilimani Safety Network", type: "Urban Security", icon: Shield },
    { name: "Super Metro Transit SACCO", type: "Commuter Corridor", icon: Bus },
    { name: "ChipuRobo Hardware Lab", type: "Hardware R&D", icon: Cpu },
  ];

  return (
    <section className="relative py-14 bg-[#050b07] border-y border-emerald-500/10 overflow-hidden">
      <div className="max-w-6xl mx-auto px-4 mb-6 text-center">
        <span className="text-xs font-mono uppercase tracking-widest text-neutral-400">
          Trusted by African Transit SACCOs, Estates, and Municipal Hubs
        </span>
      </div>

      <div className="flex overflow-hidden select-none [mask-image:linear-gradient(to_right,transparent,black_15%,black_85%,transparent)]">
        <div className="flex shrink-0 items-center gap-8 py-2 animate-marquee">
          {partners.concat(partners).map((partner, idx) => {
            const Icon = partner.icon;
            return (
              <div
                key={idx}
                className="flex items-center gap-3 px-5 py-2.5 rounded-full bg-[#08150d] border border-emerald-500/15 hover:border-emerald-500/35 transition-colors shrink-0"
              >
                <Icon className="w-4 h-4 text-emerald-400" />
                <span className="text-xs font-semibold text-white tracking-wide">
                  {partner.name}
                </span>
                <span className="text-[10px] font-mono text-emerald-400/80 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-500/20">
                  {partner.type}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
