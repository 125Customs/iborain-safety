"use client";

import React from "react";
import { Shield, Lock, FileCheck, ArrowUp } from "lucide-react";

export function Footer() {
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <footer className="relative py-16 px-4 bg-[#030704] border-t border-emerald-500/15 text-neutral-400 text-xs">
      <div className="max-w-6xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-10 pb-12 border-b border-emerald-500/10">
          
          {/* Brand Col */}
          <div className="md:col-span-5 flex flex-col justify-between">
            <div>
              <div className="flex items-center gap-3 mb-4">
                <div className="w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
                  <Shield className="w-4 h-4" />
                </div>
                <span className="text-sm font-bold tracking-wider uppercase text-white font-mono">
                  Iborain Safety
                </span>
              </div>
              <p className="text-neutral-400 font-light leading-relaxed max-w-sm">
                Decentralized solar-ready edge AI sentry grid engineered for African transit corridors,
                business districts, and gated communities. Powered by Sony IMX500 and Google Gemini 3.7 Flash.
              </p>
            </div>

            <div className="mt-6 flex items-center gap-3 text-[11px] font-mono text-emerald-400">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              <span>Nairobi Grid Sentry Node Mesh v1.4 Active</span>
            </div>
          </div>

          {/* Links Col 1: System */}
          <div className="md:col-span-2 space-y-3">
            <span className="text-xs font-mono uppercase tracking-widest text-white font-semibold block mb-2">
              Architecture
            </span>
            <ul className="space-y-2">
              <li>
                <a href="#features" className="hover:text-emerald-400 transition-colors">
                  Sony IMX500 AI
                </a>
              </li>
              <li>
                <a href="#features" className="hover:text-emerald-400 transition-colors">
                  Multimodal Reasoning
                </a>
              </li>
              <li>
                <a href="#hardware" className="hover:text-emerald-400 transition-colors">
                  Solar Canopy Kit
                </a>
              </li>
              <li>
                <a href="#hardware" className="hover:text-emerald-400 transition-colors">
                  Acoustic Strobe Pack
                </a>
              </li>
              <li>
                <a href="#terminal" className="hover:text-emerald-400 transition-colors">
                  FreeForm™ Terminal
                </a>
              </li>
            </ul>
          </div>

          {/* Links Col 2: Deployments */}
          <div className="md:col-span-2 space-y-3">
            <span className="text-xs font-mono uppercase tracking-widest text-white font-semibold block mb-2">
              Deployments
            </span>
            <ul className="space-y-2">
              <li>
                <a href="#corridors" className="hover:text-emerald-400 transition-colors">
                  Mombasa Road SACCO
                </a>
              </li>
              <li>
                <a href="#corridors" className="hover:text-emerald-400 transition-colors">
                  Eastleigh Commercial
                </a>
              </li>
              <li>
                <a href="#corridors" className="hover:text-emerald-400 transition-colors">
                  Syokimau Estate Mesh
                </a>
              </li>
              <li>
                <a href="#pricing" className="hover:text-emerald-400 transition-colors">
                  M-Pesa Subscription
                </a>
              </li>
            </ul>
          </div>

          {/* Links Col 3: Legal & Governance */}
          <div className="md:col-span-3 space-y-3">
            <span className="text-xs font-mono uppercase tracking-widest text-white font-semibold block mb-2">
              Governance & Compliance
            </span>
            <ul className="space-y-2">
              <li className="flex items-center gap-2">
                <FileCheck className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                <span>Kenya ODPC Certified 2026</span>
              </li>
              <li className="flex items-center gap-2">
                <Lock className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                <span>Zero Raw Video Retention</span>
              </li>
              <li className="flex items-center gap-2">
                <Shield className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                <span>SHA-256 Cryptographic Chain</span>
              </li>
            </ul>
          </div>

        </div>

        {/* Bottom Bar */}
        <div className="pt-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-[11px] font-mono text-neutral-500">
          <div>
            &copy; 2026 Iborain Safety Technologies. Sovereign African Sentry Grid.
          </div>
          <button
            onClick={scrollToTop}
            className="flex items-center gap-1.5 text-neutral-400 hover:text-emerald-400 transition-colors cursor-pointer"
          >
            <span>Back to top</span>
            <ArrowUp className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </footer>
  );
}
