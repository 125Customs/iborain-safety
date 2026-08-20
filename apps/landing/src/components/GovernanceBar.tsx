"use client";

import React from "react";
import { Lock, FileCheck, Server, ShieldCheck, KeyRound } from "lucide-react";

export function GovernanceBar() {
  const pillars = [
    {
      icon: ShieldCheck,
      title: "Kenya ODPC Certified",
      desc: "Full statutory compliance with Kenya Data Protection Act 2019.",
    },
    {
      icon: Lock,
      title: "Zero Video Retention",
      desc: "Raw footage converted to vector metadata on-device and purged in 30ms.",
    },
    {
      icon: KeyRound,
      title: "Cryptographic Chain",
      desc: "Immutable SHA-256 evidence hashing for court-admissible forensic audit.",
    },
    {
      icon: Server,
      title: "Community Custody",
      desc: "Data owned directly by SACCO transit operators and resident associations.",
    },
    {
      icon: FileCheck,
      title: "Zero Backdoors",
      desc: "100% sovereign African edge deployment without foreign data export.",
    },
  ];

  return (
    <section id="governance" className="relative py-16 border-y border-emerald-500/15 bg-[#07120a]/80 backdrop-blur-md">
      <div className="max-w-6xl mx-auto px-4">
        {/* Header with Date Seal */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-10 pb-6 border-b border-emerald-500/10">
          <div>
            <span className="text-xs font-mono uppercase tracking-widest text-emerald-400 font-semibold block mb-1">
              Data Sovereignty & Constitutional Governance
            </span>
            <h2 className="text-xl sm:text-2xl font-bold text-white tracking-tight">
              The 5-Pillar African Privacy Standard
            </h2>
          </div>
          <div className="inline-flex items-center gap-3 px-4 py-2 rounded-xl bg-emerald-950/40 border border-emerald-500/20 text-xs font-mono text-neutral-300 shrink-0">
            <span className="w-2 h-2 rounded-full bg-emerald-400" />
            <span>Audit Seal Validated: <strong>August 14, 2026</strong></span>
          </div>
        </div>

        {/* 5 Columns */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-6">
          {pillars.map((pillar, idx) => {
            const Icon = pillar.icon;
            return (
              <div
                key={idx}
                className="flex flex-col gap-2.5 p-4 rounded-xl glass-panel border border-emerald-500/10 hover:border-emerald-500/30 transition-all duration-300 group"
              >
                <div className="w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 group-hover:scale-105 transition-transform">
                  <Icon className="w-4 h-4" />
                </div>
                <h3 className="text-sm font-semibold text-white tracking-tight">
                  {pillar.title}
                </h3>
                <p className="text-xs text-neutral-400 leading-relaxed">
                  {pillar.desc}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
