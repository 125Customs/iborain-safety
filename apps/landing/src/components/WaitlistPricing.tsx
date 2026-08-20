"use client";

import React, { useState } from "react";
import { ShieldCheck, Check, ArrowRight, Zap, Phone, Building2, MapPin, Sparkles, CheckCircle2, Video, Sun, Cpu } from "lucide-react";
import confetti from "canvas-confetti";

export function WaitlistPricing() {
  const [selectedPlan, setSelectedPlan] = useState<"packageA" | "packageB" | "packageC">("packageA");
  const [unitCount, setUnitCount] = useState<number>(4);
  const [formSubmitted, setFormSubmitted] = useState(false);
  const [formData, setFormData] = useState({
    name: "",
    org: "",
    phone: "",
    email: "",
    location: "Nairobi (Mombasa Rd / Syokimau / Eastleigh)",
  });

  const planDetails = {
    packageA: {
      name: "Package A: Grid Sentry",
      price: 49,
      unitLabel: "Gate Sentry Node",
      badge: "Most Popular for Estates",
      desc: "For residential estate gates, school entrances, and facilities with existing wall power. Zero upfront CapEx.",
      kesPrice: 6500,
      icon: Cpu,
      inclusions: [
        "Zero CapEx Hardware (Unified Core Box + 12MP Neural Camera)",
        "Sub-30ms Onboard Sony IMX500 Neural Multimodal Vision",
        "Google Gemini 3.7 Flash FreeForm™ Crime Search Access",
        "Real-Time WhatsApp Security Incident Dispatch Group",
        "Continuous 4G LTE IoT SIM & Wi-Fi Dual Connectivity",
        "Kenya ODPC Data Sovereignty & 14-Day Local Storage Loop",
        "24-Hour Hardware Replacement & Anti-Theft IMU Tracking",
      ],
    },
    packageB: {
      name: "Package B: Solar Sentry",
      price: 99,
      unitLabel: "Solar Highway Node",
      badge: "100% Off-Grid Highway",
      desc: "For public street light poles, arterial feeder roads, and transport SACCO stages with zero grid power.",
      kesPrice: 12870,
      icon: Sun,
      inclusions: [
        "100% Off-Grid 30W Monocrystalline Solar Roof & Mount",
        "12V LiFePO4 Battery Pack with 72-Hour Rainy Weather Buffer",
        "30m High-Power 850nm Infrared Night-Vision Illuminator",
        "High-Speed Highway Capture (>120 km/h) & Doppler Radar",
        "Dual-SIM 4G LTE Auto-Failover (Safaricom / Airtel)",
        "Inter-Community 10km Mesh Vector Synchronization",
        "Automated WhatsApp Patrol Dispatch & FreeForm™ Search",
      ],
    },
    packageC: {
      name: "Package C: Smart CCTV Cloud",
      price: 20,
      unitLabel: "Connected CCTV Camera",
      badge: "Pure Cloud SaaS ($0 Hardware)",
      desc: "For hospitals, shopping malls, and estates with existing Hikvision/Dahua CCTVs. Turn old cameras into AI sentries.",
      kesPrice: 2600,
      icon: Video,
      inclusions: [
        "Zero New Hardware to Buy ($0 CapEx - Software Only)",
        "Instant RTSP Stream Ingestion for Hikvision, Dahua, Axis & Uniview",
        "Gemini 3.7 Flash Vehicle, Boda Boda, & Pedestrian AI Profiling",
        "Real-Time WhatsApp Threat Alert Dispatch for Guard Booths",
        "Natural Language FreeForm™ CCTV Video Search Engine",
        "Hospital & Logistics Priority Vehicle / Ambulance Clearance",
        "Unlimited Security Guard Seats on WhatsApp & Web Portal",
      ],
    },
  };

  const currentPlan = planDetails[selectedPlan];
  const monthlyTotal = unitCount * currentPlan.price;
  const monthlyTotalKes = unitCount * currentPlan.kesPrice;

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

  return (
    <section id="pricing" className="relative py-28 md:py-40 px-4 bg-[#050c07] border-t border-emerald-500/10">
      <div className="max-w-6xl mx-auto">
        
        {/* Section Header */}
        <div className="flex flex-col items-center text-center mb-16 md:mb-20">
          <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-xs font-mono text-emerald-400 font-medium mb-3">
            <Zap className="w-3.5 h-3.5 text-emerald-400" />
            Automated M-Pesa Micro-Subscriptions
          </div>
          <h2 className="text-3xl sm:text-5xl font-bold text-white tracking-tight max-w-3xl">
            Transparent Pricing. Zero CapEx. Instant Setup.
          </h2>
          <p className="mt-4 text-base sm:text-lg text-neutral-400 max-w-2xl font-light">
            Deploy off-grid AI sentry nodes or convert your existing CCTVs into Gemini-powered intelligence with automated monthly M-Pesa billing.
          </p>

          {/* Plan Selector Tabs */}
          <div className="mt-10 flex flex-wrap justify-center gap-3 p-1.5 rounded-2xl bg-[#08150d] border border-emerald-500/20">
            <button
              onClick={() => setSelectedPlan("packageA")}
              className={`px-5 py-2.5 rounded-xl text-xs sm:text-sm font-mono font-medium transition-all ${
                selectedPlan === "packageA"
                  ? "bg-emerald-500 text-black font-bold shadow-lg shadow-emerald-500/20"
                  : "text-neutral-300 hover:text-white hover:bg-emerald-950/40"
              }`}
            >
              Package A: Grid Sentry ($49/mo)
            </button>
            <button
              onClick={() => setSelectedPlan("packageB")}
              className={`px-5 py-2.5 rounded-xl text-xs sm:text-sm font-mono font-medium transition-all ${
                selectedPlan === "packageB"
                  ? "bg-emerald-500 text-black font-bold shadow-lg shadow-emerald-500/20"
                  : "text-neutral-300 hover:text-white hover:bg-emerald-950/40"
              }`}
            >
              Package B: Solar Sentry ($99/mo)
            </button>
            <button
              onClick={() => setSelectedPlan("packageC")}
              className={`px-5 py-2.5 rounded-xl text-xs sm:text-sm font-mono font-medium transition-all ${
                selectedPlan === "packageC"
                  ? "bg-emerald-500 text-black font-bold shadow-lg shadow-emerald-500/20"
                  : "text-neutral-300 hover:text-white hover:bg-emerald-950/40"
              }`}
            >
              Package C: Smart CCTV Cloud ($20/cam/mo)
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          {/* Left Column: Plan Overview & Inclusions */}
          <div className="lg:col-span-6 p-8 rounded-3xl glass-panel border border-emerald-500/25 bg-[#07130a]/90 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between gap-4 mb-6">
                <span className="text-xs font-mono uppercase tracking-widest text-emerald-400 font-semibold">
                  {currentPlan.badge}
                </span>
                <span className="text-xs font-mono text-neutral-400 bg-[#040c06] px-3 py-1 rounded-full border border-emerald-500/15">
                  M-Pesa STK Push / Card
                </span>
              </div>

              <div className="mb-6">
                <div className="flex items-baseline gap-2">
                  <span className="text-5xl sm:text-6xl font-black text-white font-mono tracking-tight">
                    ${monthlyTotal}
                  </span>
                  <span className="text-sm text-neutral-400 font-mono">
                    / month ({unitCount} {unitCount === 1 ? currentPlan.unitLabel : `${currentPlan.unitLabel}s`})
                  </span>
                </div>
                <p className="text-xs text-emerald-400 font-mono mt-1">
                  KES ~{monthlyTotalKes.toLocaleString()} per month billed via automated M-Pesa prompt
                </p>
                <p className="text-xs text-neutral-300 font-light mt-3">
                  {currentPlan.desc}
                </p>
              </div>

              {/* Unit Slider */}
              <div className="p-5 rounded-2xl bg-[#030904] border border-emerald-500/15 mb-8">
                <div className="flex items-center justify-between text-xs font-mono text-neutral-300 mb-3">
                  <span>Deployment Scale:</span>
                  <span className="text-emerald-400 font-bold">{unitCount} {unitCount === 1 ? "Unit" : "Units"}</span>
                </div>
                <input
                  type="range"
                  min="1"
                  max="20"
                  value={unitCount}
                  onChange={(e) => setUnitCount(parseInt(e.target.value))}
                  className="w-full h-2 bg-emerald-950 rounded-lg appearance-none cursor-pointer accent-emerald-400"
                />
                <div className="flex justify-between text-[10px] font-mono text-neutral-500 mt-2">
                  <span>1 Unit</span>
                  <span>10 Units</span>
                  <span>20+ Enterprise</span>
                </div>
              </div>

              {/* Inclusions List */}
              <div className="space-y-3 pt-6 border-t border-emerald-500/15">
                <h4 className="text-xs font-mono uppercase tracking-widest text-neutral-400 mb-4">
                  Everything Included in Your Subscription:
                </h4>
                {currentPlan.inclusions.map((item, idx) => (
                  <div key={idx} className="flex items-start gap-3 text-xs sm:text-sm text-neutral-200 font-light">
                    <Check className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                    <span>{item}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="mt-8 pt-6 border-t border-emerald-500/15 flex items-center gap-3 text-xs font-mono text-neutral-400">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              <span>14-Day Zero-Risk Trial • No Long-Term Lock-in</span>
            </div>
          </div>

          {/* Right Column: Deployment Form */}
          <div className="lg:col-span-6 p-8 rounded-3xl glass-panel border border-emerald-500/25 bg-[#07130a]/90">
            {formSubmitted ? (
              <div className="py-16 text-center flex flex-col items-center">
                <div className="w-16 h-16 rounded-full bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-emerald-400 mb-6">
                  <CheckCircle2 className="w-8 h-8" />
                </div>
                <h3 className="text-2xl font-bold text-white mb-2">Pilot Request Submitted!</h3>
                <p className="text-sm text-neutral-300 font-light max-w-md mb-6 leading-relaxed">
                  Thank you, <span className="text-white font-medium">{formData.name}</span>. Our Nairobi deployment team will contact you at <span className="text-emerald-400 font-mono">{formData.phone}</span> within 2 hours to schedule your 14-day zero-cost pilot installation.
                </p>
                <div className="p-4 rounded-xl bg-[#030904] border border-emerald-500/20 text-xs font-mono text-neutral-400 text-left w-full max-w-sm space-y-1.5">
                  <div><b>Package:</b> {currentPlan.name}</div>
                  <div><b>Scale:</b> {unitCount} Units</div>
                  <div><b>Target Location:</b> {formData.location}</div>
                  <div><b>Setup Cost:</b> KES 0 (14-Day Free Pilot)</div>
                </div>
              </div>
            ) : (
              <div>
                <div className="mb-6">
                  <span className="text-xs font-mono uppercase tracking-widest text-emerald-400 font-semibold block mb-1">
                    Direct Pilot Onboarding
                  </span>
                  <h3 className="text-2xl font-bold text-white tracking-tight">
                    Schedule Your 14-Day Risk-Free Pilot
                  </h3>
                  <p className="text-xs text-neutral-400 font-light mt-1">
                    We install the system at your gate, pole, or hospital for KES 0. If you do not love it, we uninstall it for free.
                  </p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-4">
                  <div>
                    <label className="block text-xs font-mono text-neutral-300 mb-1.5">Full Name / Contact Person *</label>
                    <input
                      type="text"
                      required
                      placeholder="e.g. Samuel Otieno (Security Chairman)"
                      value={formData.name}
                      onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                      className="w-full px-4 py-3 rounded-xl bg-[#030904] border border-emerald-500/20 text-sm text-white focus:outline-none focus:border-emerald-400 font-light"
                    />
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-xs font-mono text-neutral-300 mb-1.5">M-Pesa Phone Number *</label>
                      <div className="relative">
                        <Phone className="w-4 h-4 text-neutral-500 absolute left-3.5 top-3.5" />
                        <input
                          type="tel"
                          required
                          placeholder="+254 712 345 678"
                          value={formData.phone}
                          onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                          className="w-full pl-10 pr-4 py-3 rounded-xl bg-[#030904] border border-emerald-500/20 text-sm text-white focus:outline-none focus:border-emerald-400 font-light"
                        />
                      </div>
                    </div>

                    <div>
                      <label className="block text-xs font-mono text-neutral-300 mb-1.5">Estate / Facility / SACCO *</label>
                      <div className="relative">
                        <Building2 className="w-4 h-4 text-neutral-500 absolute left-3.5 top-3.5" />
                        <input
                          type="text"
                          required
                          placeholder="e.g. Syokimau Court 4 / KNH"
                          value={formData.org}
                          onChange={(e) => setFormData({ ...formData, org: e.target.value })}
                          className="w-full pl-10 pr-4 py-3 rounded-xl bg-[#030904] border border-emerald-500/20 text-sm text-white focus:outline-none focus:border-emerald-400 font-light"
                        />
                      </div>
                    </div>
                  </div>

                  <div>
                    <label className="block text-xs font-mono text-neutral-300 mb-1.5">Corridor / Location in Kenya</label>
                    <div className="relative">
                      <MapPin className="w-4 h-4 text-neutral-500 absolute left-3.5 top-3.5" />
                      <select
                        value={formData.location}
                        onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                        className="w-full pl-10 pr-4 py-3 rounded-xl bg-[#030904] border border-emerald-500/20 text-sm text-white focus:outline-none focus:border-emerald-400 font-light appearance-none"
                      >
                        <option value="Nairobi (Mombasa Rd / Syokimau / Athi River)">Nairobi (Mombasa Rd / Syokimau / Athi River)</option>
                        <option value="Nairobi (Thika Superhighway / Ruiru / Juja)">Nairobi (Thika Superhighway / Ruiru / Juja)</option>
                        <option value="Nairobi (Northern Bypass / Membley / Kiambu)">Nairobi (Northern Bypass / Membley / Kiambu)</option>
                        <option value="Nairobi (Westlands / Karen / Runda / Kilimani)">Nairobi (Westlands / Karen / Runda / Kilimani)</option>
                        <option value="Hospital / Commercial CCTV Integration (Nationwide)">Hospital / Commercial CCTV Integration (Nationwide)</option>
                        <option value="Other County / Municipality">Other County / Municipality</option>
                      </select>
                    </div>
                  </div>

                  <button
                    type="submit"
                    className="w-full mt-6 py-4 rounded-xl bg-emerald-400 text-black font-mono font-bold text-sm hover:bg-emerald-300 transition-all flex items-center justify-center gap-2 shadow-lg shadow-emerald-500/25"
                  >
                    <span>Request 14-Day Zero-Cost Pilot Installation</span>
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </form>
              </div>
            )}
          </div>

        </div>

      </div>
    </section>
  );
}
