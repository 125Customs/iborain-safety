"use client";

import React, { useState } from "react";
import { ShieldCheck, Check, ArrowRight, Zap, Phone, Building2, MapPin, Sparkles, CheckCircle2 } from "lucide-react";
import confetti from "canvas-confetti";

export function WaitlistPricing() {
  const [nodeCount, setNodeCount] = useState<number>(4);
  const [formSubmitted, setFormSubmitted] = useState(false);
  const [formData, setFormData] = useState({
    name: "",
    org: "",
    phone: "",
    email: "",
    location: "Nairobi (Mombasa Rd / Syokimau / Eastleigh)",
  });

  const pricePerNode = 49;
  const monthlyTotal = nodeCount * pricePerNode;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.name || !formData.phone) return;

    setFormSubmitted(true);
    try {
      confetti({
        particleCount: 80,
        spread: 70,
        origin: { y: 0.6 },
        colors: ["#10b981", "#34d399", "#00f090", "#ffffff"],
      });
    } catch {
      // ignore
    }
  };

  const inclusions = [
    "Zero CapEx Hardware (Sentry One + Solar Canopy Kit + Strobe Pack)",
    "Sub-30ms Onboard Sony IMX500 Neural Multimodal Vision",
    "Google Gemini 3.7 Flash FreeForm™ Crime Search Access",
    "Decentralized 10km Inter-Community Mesh & Hotlist Sync",
    "Automated WhatsApp Patrol Dispatch Bot with Location Pinning",
    "Built-in 4G/LTE-M Telemetry & Solar Power with 48h Rainy Buffer",
    "Kenya ODPC Data Sovereignty Compliance & SHA-256 Audit Hashes",
    "24-Hour Hardware Replacement Guarantee & Anti-Theft Gyro Tracking",
  ];

  return (
    <section id="pricing" className="relative py-28 md:py-40 px-4 bg-[#050c07] border-t border-emerald-500/10">
      <div className="max-w-6xl mx-auto">
        
        {/* Section Header */}
        <div className="flex flex-col items-center text-center mb-16 md:mb-24">
          <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-xs font-mono text-emerald-400 font-medium mb-3">
            <Zap className="w-3.5 h-3.5 text-emerald-400" />
            Automated M-Pesa Micro-Subscriptions
          </div>
          <h2 className="text-3xl sm:text-5xl font-bold text-white tracking-tight max-w-3xl">
            Zero Upfront CapEx. All-Inclusive $49/Month Per Node.
          </h2>
          <p className="mt-4 text-base sm:text-lg text-neutral-400 max-w-2xl font-light">
            No expensive servers, no fiber trenching, no hidden data fees. Deploy complete solar-ready AI sentry nodes
            with transparent automated billing.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          {/* Left Column: Plan Overview & Inclusions */}
          <div className="lg:col-span-6 p-8 rounded-3xl glass-panel border border-emerald-500/25 bg-[#07130a]/90 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between gap-4 mb-6">
                <span className="text-xs font-mono uppercase tracking-widest text-emerald-400 font-semibold">
                  Community & Corridor Plan
                </span>
                <span className="text-xs font-mono text-neutral-400 bg-[#040c06] px-3 py-1 rounded-full border border-emerald-500/15">
                  M-Pesa / Card / Bank
                </span>
              </div>

              <div className="mb-6">
                <div className="flex items-baseline gap-2">
                  <span className="text-5xl sm:text-6xl font-black text-white font-mono tracking-tight">
                    ${monthlyTotal}
                  </span>
                  <span className="text-sm text-neutral-400 font-mono">
                    / month ({nodeCount} {nodeCount === 1 ? "Node" : "Nodes"})
                  </span>
                </div>
                <p className="text-xs text-emerald-400 font-mono mt-1">
                  KES ~{(monthlyTotal * 130).toLocaleString()} per month billed via automated M-Pesa prompt
                </p>
              </div>

              {/* Node Slider */}
              <div className="p-5 rounded-2xl bg-[#030904] border border-emerald-500/15 mb-8">
                <div className="flex items-center justify-between text-xs font-mono text-neutral-300 mb-3">
                  <span>Hardware Grid Scale:</span>
                  <span className="text-emerald-400 font-bold">{nodeCount} Sentry Units</span>
                </div>
                <input
                  type="range"
                  min={1}
                  max={20}
                  value={nodeCount}
                  onChange={(e) => setNodeCount(parseInt(e.target.value))}
                  className="w-full h-2 bg-[#0d2616] rounded-lg appearance-none cursor-pointer accent-emerald-400"
                />
                <div className="flex justify-between text-[10px] font-mono text-neutral-500 mt-2">
                  <span>1 Node (Single Gate)</span>
                  <span>4 Nodes (Estate Quad)</span>
                  <span>12+ Nodes (SACCO Corridor)</span>
                </div>
              </div>

              {/* Feature Checklist */}
              <div className="space-y-3 pt-2">
                <span className="text-xs font-mono text-neutral-400 uppercase tracking-wider block mb-2">
                  Included in Every Node Subscription:
                </span>
                {inclusions.map((item, idx) => (
                  <div key={idx} className="flex items-start gap-2.5 text-xs text-neutral-200">
                    <Check className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                    <span>{item}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Right Column: Pre-Order Waitlist Application Form */}
          <div className="lg:col-span-6 p-8 sm:p-10 rounded-3xl glass-panel border border-emerald-500/30 bg-[#08150d] shadow-2xl relative">
            
            {formSubmitted ? (
              <div className="py-12 flex flex-col items-center text-center space-y-4">
                <div className="w-16 h-16 rounded-full bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-emerald-400 mb-2">
                  <CheckCircle2 className="w-8 h-8" />
                </div>
                <h3 className="text-2xl font-bold text-white tracking-tight">
                  Node Reservation Confirmed
                </h3>
                <p className="text-sm text-neutral-300 max-w-md font-light leading-relaxed">
                  Thank you, <strong>{formData.name}</strong>. Your priority waitlist allocation for{" "}
                  <strong>{nodeCount} Iborain Sentry Nodes</strong> has been registered. Our regional deployment coordinator will contact you via WhatsApp ({formData.phone}) with site survey dates.
                </p>
                <div className="p-4 rounded-xl bg-[#030904] border border-emerald-500/20 text-xs font-mono text-emerald-400 text-left w-full mt-4 space-y-1">
                  <div>ALLOCATION_ID: IBR-{Math.floor(100000 + Math.random() * 900000)}</div>
                  <div>GRID_TARGET: {formData.location}</div>
                  <div>SUBSCRIPTION_EST: ${monthlyTotal}/month (KES ~{(monthlyTotal * 130).toLocaleString()})</div>
                </div>
                <button
                  onClick={() => setFormSubmitted(false)}
                  className="mt-4 text-xs font-mono text-neutral-400 hover:text-emerald-400 underline cursor-pointer"
                >
                  Submit another reservation
                </button>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <span className="text-xs font-mono uppercase tracking-widest text-emerald-400 font-semibold block mb-1">
                    Priority Node Allocation
                  </span>
                  <h3 className="text-2xl font-bold text-white tracking-tight mb-2">
                    Join the Deployment Waitlist
                  </h3>
                  <p className="text-xs text-neutral-400 font-light mb-6">
                    Pilot hardware nodes are deployed on a rolling basis across Kenyan corridors. Reserve your sector priority.
                  </p>
                </div>

                {/* Name */}
                <div>
                  <label className="block text-xs font-mono text-neutral-300 mb-1.5">
                    Contact Name / Estate Security Representative *
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    placeholder="e.g. David Mwangi"
                    className="w-full px-4 py-3 rounded-xl bg-[#040b06] border border-emerald-500/20 text-white text-xs sm:text-sm focus:outline-none focus:border-emerald-400 transition-colors"
                  />
                </div>

                {/* Organization / Estate */}
                <div>
                  <label className="block text-xs font-mono text-neutral-300 mb-1.5">
                    Estate / SACCO / Commercial Hub Name
                  </label>
                  <input
                    type="text"
                    value={formData.org}
                    onChange={(e) => setFormData({ ...formData, org: e.target.value })}
                    placeholder="e.g. Syokimau West Residents Association"
                    className="w-full px-4 py-3 rounded-xl bg-[#040b06] border border-emerald-500/20 text-white text-xs sm:text-sm focus:outline-none focus:border-emerald-400 transition-colors"
                  />
                </div>

                {/* Phone & Email Grid */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-mono text-neutral-300 mb-1.5">
                      M-Pesa Phone Number *
                    </label>
                    <input
                      type="tel"
                      required
                      value={formData.phone}
                      onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                      placeholder="+254 7XX XXX XXX"
                      className="w-full px-4 py-3 rounded-xl bg-[#040b06] border border-emerald-500/20 text-white text-xs sm:text-sm focus:outline-none focus:border-emerald-400 transition-colors"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-mono text-neutral-300 mb-1.5">
                      Email Address
                    </label>
                    <input
                      type="email"
                      value={formData.email}
                      onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                      placeholder="security@estate.co.ke"
                      className="w-full px-4 py-3 rounded-xl bg-[#040b06] border border-emerald-500/20 text-white text-xs sm:text-sm focus:outline-none focus:border-emerald-400 transition-colors"
                    />
                  </div>
                </div>

                {/* Location Selection */}
                <div>
                  <label className="block text-xs font-mono text-neutral-300 mb-1.5">
                    Deployment Corridor / Region
                  </label>
                  <select
                    value={formData.location}
                    onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                    className="w-full px-4 py-3 rounded-xl bg-[#040b06] border border-emerald-500/20 text-white text-xs sm:text-sm focus:outline-none focus:border-emerald-400 transition-colors"
                  >
                    <option value="Nairobi (Mombasa Rd / Syokimau / Eastleigh)">
                      Nairobi (Mombasa Rd / Syokimau / Eastleigh / Westlands)
                    </option>
                    <option value="Mombasa Coastal Corridor">Mombasa Coastal Corridor (Nyali / Bamburi / Port)</option>
                    <option value="Nakuru Rift Transit Corridor">Nakuru Rift Transit Corridor</option>
                    <option value="Kisumu Western Transit Hub">Kisumu Western Transit Hub</option>
                    <option value="Eldoret / North Rift Corridor">Eldoret / North Rift Corridor</option>
                  </select>
                </div>

                {/* Submit CTA */}
                <button
                  type="submit"
                  className="w-full mt-4 py-4 rounded-xl text-sm font-bold text-black bg-gradient-to-r from-emerald-400 via-emerald-300 to-teal-400 hover:opacity-95 transition-all shadow-xl shadow-emerald-500/25 flex items-center justify-center gap-2 group cursor-pointer active:scale-95"
                >
                  <span>Lock In {nodeCount} Sentry Node Reservation</span>
                  <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
                </button>

                <p className="text-center text-[11px] font-mono text-neutral-500 mt-2">
                  Zero commitment. No payment required until on-site pole deployment.
                </p>
              </form>
            )}

          </div>

        </div>

      </div>
    </section>
  );
}
