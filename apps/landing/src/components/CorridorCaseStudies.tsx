"use client";

import React, { useState } from "react";
import { MapPin, MessageSquare, Clock, ShieldCheck, ArrowUpRight, CheckCheck } from "lucide-react";

interface CaseStudy {
  id: string;
  location: string;
  category: string;
  metric: string;
  metricLabel: string;
  headline: string;
  narrative: string;
  whatsappMessage: {
    sender: string;
    timestamp: string;
    body: string;
    status: string;
  };
}

export function CorridorCaseStudies() {
  const caseStudies: CaseStudy[] = [
    {
      id: "mombasa-rd",
      location: "Mombasa Road Arterial",
      category: "SACCO Logistics Corridor",
      metric: "2m 40s",
      metricLabel: "Patrol Intercept Time",
      headline: "Stolen Cargo Interception via Roof Rack Geometry",
      narrative:
        "When an unplated commercial van with obscured rear identification passed the Southern Bypass interchange, Sentry Node #08 fingerprinted its welded roof rack and left rear quarter dent, alerting SACCO route patrol units instantly.",
      whatsappMessage: {
        sender: "Iborain Bot • Mombasa Rd Sentry Grid",
        timestamp: "03:18 AM",
        body: "FLAGGED TRANSIT ALERT: Unplated White Toyota Probox with commercial roof rack and dark tints entered Mombasa Rd Southbound at 64km/h. Matched Hotlist #LARCENY-7712. Intercept dispatched.",
        status: "Delivered to 18 Patrol Units",
      },
    },
    {
      id: "eastleigh",
      location: "Eastleigh Commercial Hub",
      category: "High-Density Business District",
      metric: "100%",
      metricLabel: "Off-Hours Gas Theft Deterrence",
      headline: "Automated Verbal Warning Halts Unauthorized Night Ingress",
      narrative:
        "At 02:14 AM, an unplated motorbike carrying two 13kg gas cylinders attempted entry into a commercial storage alley. Sentry Node #03 triggered the 120Hz radar strobe and verbal Swahili acoustic warning, forcing immediate retreat.",
      whatsappMessage: {
        sender: "Iborain Bot • Eastleigh Commercial Grid",
        timestamp: "02:14 AM",
        body: "ACTIVE DETERRENCE TRIGGERED: Unplated Boda Boda (Red Boxer 150) carrying 2x 13kg LPG cylinders approached 12th Street Alley. Verbal warning sounded. Target retreated toward Ring Road.",
        status: "Logged & Archived with Video Hash",
      },
    },
    {
      id: "syokimau",
      location: "Syokimau Perimeter Grid",
      category: "Gated Estate Mesh",
      metric: "89%",
      metricLabel: "Drop in Perimeter Intrusions",
      headline: "14-Node Decentralized Mesh Seals Estate Access Roads",
      narrative:
        "14 solar sentry nodes deployed across estate access gates maintain a 10km regional mesh. When a suspicious vehicle was flagged on Mombasa Road, Syokimau estate barriers were automatically notified before arrival.",
      whatsappMessage: {
        sender: "Iborain Bot • Syokimau Estate Security",
        timestamp: "11:42 PM",
        body: "REGIONAL MESH SYNC: Flagged hotlist vehicle FP-TOY-SILVER-401 approaching North Gate in estimated 180s. Security barrier pre-locked. Static guard notified.",
        status: "Confirmed by Gate 1 Captain",
      },
    },
  ];

  const [activeStudy, setActiveStudy] = useState<CaseStudy>(caseStudies[0]);

  return (
    <section id="corridors" className="relative py-28 md:py-40 px-4 bg-[#050c07] border-t border-emerald-500/10">
      <div className="max-w-6xl mx-auto">
        
        {/* Section Header */}
        <div className="flex flex-col items-center text-center mb-16 md:mb-24">
          <span className="text-xs font-mono uppercase tracking-widest text-emerald-400 font-semibold mb-3">
            Real-World Corridor Deployments
          </span>
          <h2 className="text-3xl sm:text-5xl font-bold text-white tracking-tight max-w-3xl">
            Location-Pinned Field Evidence & Instant WhatsApp Dispatch
          </h2>
          <p className="mt-4 text-base sm:text-lg text-neutral-400 max-w-2xl font-light">
            See how neighborhood associations, business corridors, and SACCO transit fleets leverage Iborain
            sentry nodes for instant incident containment.
          </p>
        </div>

        {/* Location Selector Tabs */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-10">
          {caseStudies.map((study) => (
            <button
              key={study.id}
              onClick={() => setActiveStudy(study)}
              className={`p-5 rounded-2xl text-left transition-all duration-300 cursor-pointer ${
                activeStudy.id === study.id
                  ? "bg-[#091a10] border-2 border-emerald-400 shadow-xl shadow-emerald-950/50"
                  : "glass-panel border border-emerald-500/15 hover:border-emerald-500/30"
              }`}
            >
              <div className="flex items-center justify-between text-xs font-mono text-emerald-400 mb-2">
                <span className="flex items-center gap-1.5">
                  <MapPin className="w-3.5 h-3.5 text-emerald-400" />
                  {study.location}
                </span>
                <span className="font-bold text-white text-sm">{study.metric}</span>
              </div>
              <h4 className="text-sm font-semibold text-white tracking-tight">
                {study.category}
              </h4>
            </button>
          ))}
        </div>

        {/* Active Case Study Detail Box */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 p-8 sm:p-10 rounded-3xl glass-panel border border-emerald-500/20 bg-[#07130a]/90">
          
          {/* Narrative Left Column */}
          <div className="lg:col-span-7 flex flex-col justify-between">
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-xs font-mono text-emerald-400 font-medium mb-4">
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                Verified Incident Report
              </div>
              <h3 className="text-2xl sm:text-3xl font-bold text-white tracking-tight mb-4">
                {activeStudy.headline}
              </h3>
              <p className="text-sm sm:text-base text-neutral-300 font-light leading-relaxed mb-6">
                {activeStudy.narrative}
              </p>
            </div>

            <div className="grid grid-cols-2 gap-4 pt-6 border-t border-emerald-500/15">
              <div>
                <span className="text-xs font-mono text-neutral-400 block mb-1">Impact Metric</span>
                <span className="text-2xl font-bold text-emerald-400">{activeStudy.metric}</span>
                <p className="text-xs text-neutral-400 mt-0.5">{activeStudy.metricLabel}</p>
              </div>
              <div>
                <span className="text-xs font-mono text-neutral-400 block mb-1">Dispatch Latency</span>
                <span className="text-2xl font-bold text-white">&lt; 380 ms</span>
                <p className="text-xs text-neutral-400 mt-0.5">Automated WhatsApp broadcast</p>
              </div>
            </div>
          </div>

          {/* WhatsApp Dispatch Simulator Card Right Column */}
          <div className="lg:col-span-5 p-6 rounded-2xl bg-[#030a05] border border-emerald-500/25 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between pb-3 mb-4 border-b border-emerald-500/15">
                <div className="flex items-center gap-2.5">
                  <div className="w-8 h-8 rounded-full bg-emerald-600 flex items-center justify-center text-white">
                    <MessageSquare className="w-4 h-4" />
                  </div>
                  <div>
                    <span className="text-xs font-bold text-white block">WhatsApp Patrol Mesh</span>
                    <span className="text-[10px] font-mono text-emerald-400">Automated Bot Dispatch</span>
                  </div>
                </div>
                <span className="text-[10px] font-mono text-neutral-400">{activeStudy.whatsappMessage.timestamp}</span>
              </div>

              {/* Message Bubble */}
              <div className="p-4 rounded-xl rounded-tl-none bg-[#091a0f] border border-emerald-500/20 text-xs text-neutral-200 leading-relaxed font-sans shadow-md">
                <p className="font-semibold text-emerald-300 text-[11px] mb-1">
                  {activeStudy.whatsappMessage.sender}
                </p>
                <p>{activeStudy.whatsappMessage.body}</p>
                <div className="flex items-center justify-end gap-1.5 mt-2 text-[10px] text-emerald-400 font-mono">
                  <CheckCheck className="w-3.5 h-3.5 text-emerald-400" />
                  <span>{activeStudy.whatsappMessage.status}</span>
                </div>
              </div>
            </div>

            <div className="mt-4 pt-3 border-t border-emerald-500/10 flex items-center justify-between text-xs font-mono text-neutral-400">
              <span>Security Channel: ACTIVE</span>
              <span className="text-emerald-400 font-semibold">1-Tap Escalation</span>
            </div>
          </div>

        </div>

      </div>
    </section>
  );
}
