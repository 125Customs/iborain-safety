"use client";

import React, { useState } from "react";
import { Terminal, Play, Sparkles, Copy, Check, Shield, CornerDownLeft } from "lucide-react";

export function InteractiveTerminal() {
  const [query, setQuery] = useState(
    "Find unplated red Boxer 150 carrying blue 13kg gas cylinder heading toward Syokimau"
  );
  const [isExecuting, setIsExecuting] = useState(false);
  const [copied, setCopied] = useState(false);

  const sampleQueries = [
    "Find unplated red Boxer 150 carrying blue 13kg gas cylinder heading toward Syokimau",
    "Locate modified white Toyota Probox with commercial welded roof rack seen on Mombasa Road",
    "Identify any motorcycle without helmet crossing Eastleigh junction after midnight",
  ];

  const handleCopy = () => {
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleQuerySelect = (q: string) => {
    setQuery(q);
  };

  return (
    <section id="terminal" className="relative py-28 md:py-40 px-4 bg-[#050c07] border-t border-emerald-500/10">
      <div className="max-w-6xl mx-auto">
        
        {/* Section Header */}
        <div className="flex flex-col items-center text-center mb-16">
          <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-xs font-mono text-emerald-400 font-medium mb-3">
            <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
            Gemini 3.7 Flash FreeForm™ Engine
          </div>
          <h2 className="text-3xl sm:text-5xl font-bold text-white tracking-tight max-w-3xl">
            Natural Language Crime Investigation Terminal
          </h2>
          <p className="mt-4 text-base sm:text-lg text-neutral-400 max-w-2xl font-light">
            Search months of corridor movements in plain English or Swahili. Gemini 3.7 Flash analyzes 
            diff vectors across the decentralized 10km sentry mesh to pinpoint suspects without manual video review.
          </p>
        </div>

        {/* Terminal Container */}
        <div className="rounded-3xl glass-panel border border-emerald-500/25 shadow-2xl overflow-hidden bg-[#040a06]/95">
          
          {/* Terminal Window Chrome */}
          <div className="px-6 py-4 bg-[#07130a] border-b border-emerald-500/15 flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <span className="w-3 h-3 rounded-full bg-red-500/80" />
              <span className="w-3 h-3 rounded-full bg-yellow-500/80" />
              <span className="w-3 h-3 rounded-full bg-emerald-500/80" />
              <span className="ml-3 text-xs font-mono text-neutral-400">
                iborain-cli --model=gemini-3.7-flash --mesh=nairobi-grid-v1
              </span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-[11px] font-mono text-emerald-400 bg-emerald-950/60 px-2.5 py-1 rounded border border-emerald-500/20">
                10km Mesh Active
              </span>
            </div>
          </div>

          {/* Preset Prompts Selector */}
          <div className="px-6 py-3 bg-[#060e08] border-b border-emerald-500/10 flex flex-wrap items-center gap-2 text-xs font-mono">
            <span className="text-neutral-400 font-medium">Quick Investigations:</span>
            {sampleQueries.map((item, idx) => (
              <button
                key={idx}
                onClick={() => handleQuerySelect(item)}
                className="px-3 py-1 rounded-md bg-[#08170e] hover:bg-emerald-950/50 border border-emerald-500/15 hover:border-emerald-500/35 text-neutral-300 hover:text-emerald-300 transition-all text-[11px] cursor-pointer"
              >
                Query {idx + 1}
              </button>
            ))}
          </div>

          {/* Terminal Body */}
          <div className="p-6 font-mono text-xs sm:text-sm space-y-6">
            
            {/* Input Line */}
            <div className="flex items-center gap-3 p-3 rounded-xl bg-[#07150c] border border-emerald-500/20">
              <span className="text-emerald-400 font-bold">&gt;</span>
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="flex-1 bg-transparent text-white focus:outline-none font-mono text-xs sm:text-sm placeholder-neutral-500"
                placeholder="Type your natural language investigation query..."
              />
              <button
                onClick={() => {
                  setIsExecuting(true);
                  setTimeout(() => setIsExecuting(false), 300);
                }}
                className="px-4 py-1.5 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-black font-semibold font-mono text-xs flex items-center gap-1.5 cursor-pointer active:scale-95 transition-all"
              >
                <Play className="w-3 h-3 fill-black" />
                <span>Execute</span>
              </button>
            </div>

            {/* Output Stream */}
            <div className="p-5 rounded-2xl bg-[#030704] border border-emerald-500/15 text-neutral-300 space-y-4">
              <div className="flex items-center justify-between text-xs text-neutral-400 border-b border-emerald-500/10 pb-3">
                <span className="text-emerald-400 font-semibold flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                  GEMINI 3.7 FLASH MULTIMODAL REASONING ENGINE
                </span>
                <span className="font-mono text-emerald-300">EXEC_TIME: 142ms</span>
              </div>

              {/* JSON Stream Display */}
              <pre className="text-neutral-300 text-xs font-mono overflow-x-auto leading-relaxed whitespace-pre-wrap">
{`{
  "query_status": "MATCH_CONFIRMED",
  "reasoning_model": "Google Gemini 3.7 Flash Multimodal Live",
  "matched_target": {
    "vehicle_category": "MOTORCYCLE_BODA_BODA",
    "make_model": "Bajaj Boxer 150 (Black Frame / Crimson Red Tank)",
    "license_plate": {
      "status": "UNPLATED_REAR_BRACKET",
      "synthetic_fingerprint": "FP-BODA-RED-8942-SYO"
    },
    "cargo_anomaly": {
      "classified": "13kg LPG Gas Cylinder (Blue Casing)",
      "mounting": "Rear Rack Elastic Bungee Cord",
      "risk_score": 0.94
    },
    "trajectory": [
      { "node": "Mombasa-Road-Node-07", "timestamp": "2026-08-19T01:38:12+03:00", "speed_kmh": 46 },
      { "node": "Syokimau-Gate-Perimeter-02", "timestamp": "2026-08-19T01:42:04+03:00", "speed_kmh": 28 }
    ],
    "hotlist_correlation": "INTER_ESTATE_LARCENY_ALERT_#4091",
    "automated_dispatch": {
      "whatsapp_channel": "Syokimau Community Security Group",
      "dispatch_latency": "384ms",
      "patrol_action": "PERIMETER_CONTAINMENT_ACTIVE"
    }
  }
}`}
              </pre>

              <div className="pt-3 border-t border-emerald-500/10 flex items-center justify-between text-xs text-neutral-400">
                <span className="text-emerald-400">Mesh Nodes Queried: 24 (10km Radius)</span>
                <button
                  onClick={handleCopy}
                  className="flex items-center gap-1.5 text-neutral-300 hover:text-emerald-400 transition-colors cursor-pointer"
                >
                  {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                  <span>{copied ? "Copied" : "Copy Output"}</span>
                </button>
              </div>
            </div>

          </div>

        </div>

      </div>
    </section>
  );
}
