"use client";

import React, { useState, useEffect } from "react";
import { Shield, Radio, ChevronRight, Menu, X, Terminal, Cpu } from "lucide-react";

export function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const scrollToSection = (id: string) => {
    setMobileMenuOpen(false);
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <header className="fixed top-0 left-0 right-0 z-50 flex justify-center px-4 pt-4 sm:pt-6 transition-all duration-300">
      <nav
        className={`w-full max-w-6xl mx-auto flex items-center justify-between px-5 py-3 rounded-full transition-all duration-300 ${
          scrolled
            ? "glass-panel shadow-2xl shadow-black/80 border border-emerald-500/20 backdrop-blur-xl bg-[#07110a]/90"
            : "bg-[#07110a]/60 border border-emerald-500/10 backdrop-blur-md"
        }`}
      >
        {/* Brand */}
        <div
          onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
          className="flex items-center gap-3 cursor-pointer group"
        >
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-emerald-500 to-emerald-900 flex items-center justify-center p-0.5 shadow-lg shadow-emerald-950/50 group-hover:scale-105 transition-transform duration-300">
            <div className="w-full h-full bg-[#060b08] rounded-[10px] flex items-center justify-center">
              <Shield className="w-4 h-4 text-emerald-400" />
            </div>
          </div>
          <div className="flex flex-col">
            <span className="font-bold text-sm tracking-wider uppercase text-white group-hover:text-emerald-400 transition-colors">
              Iborain Safety
            </span>
            <span className="text-[10px] tracking-widest uppercase text-emerald-400/70 font-mono flex items-center gap-1.5">
              <span className="inline-block w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
              Sentry Mesh v1.4
            </span>
          </div>
        </div>

        {/* Desktop Navigation Links */}
        <div className="hidden md:flex items-center gap-7 text-xs font-medium text-neutral-300">
          <button
            onClick={() => scrollToSection("features")}
            className="hover:text-emerald-400 transition-colors cursor-pointer"
          >
            Neural AI
          </button>
          <button
            onClick={() => scrollToSection("hardware")}
            className="hover:text-emerald-400 transition-colors cursor-pointer"
          >
            Hardware Lineup
          </button>
          <button
            onClick={() => scrollToSection("terminal")}
            className="hover:text-emerald-400 transition-colors cursor-pointer flex items-center gap-1.5"
          >
            <Terminal className="w-3.5 h-3.5 text-emerald-400" />
            FreeForm™ Search
          </button>
          <button
            onClick={() => scrollToSection("corridors")}
            className="hover:text-emerald-400 transition-colors cursor-pointer"
          >
            Corridors
          </button>
          <button
            onClick={() => scrollToSection("governance")}
            className="hover:text-emerald-400 transition-colors cursor-pointer"
          >
            Data Sovereignty
          </button>
          <button
            onClick={() => scrollToSection("pricing")}
            className="hover:text-emerald-400 transition-colors cursor-pointer"
          >
            Pricing ($49/mo)
          </button>
        </div>

        {/* Action Button */}
        <div className="hidden sm:flex items-center gap-3">
          <button
            onClick={() => scrollToSection("pricing")}
            className="group relative inline-flex items-center gap-2 px-5 py-2 rounded-full text-xs font-semibold text-black bg-gradient-to-r from-emerald-400 via-emerald-300 to-teal-400 hover:opacity-95 transition-all shadow-md shadow-emerald-500/20 active:scale-95 cursor-pointer"
          >
            <span>Pre-Order Nodes</span>
            <ChevronRight className="w-3.5 h-3.5 transition-transform group-hover:translate-x-0.5" />
          </button>
        </div>

        {/* Mobile Menu Toggle */}
        <button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="md:hidden p-1.5 text-neutral-300 hover:text-white focus:outline-none"
          aria-label="Toggle menu"
        >
          {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        </button>
      </nav>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden fixed top-20 left-4 right-4 p-5 rounded-2xl glass-panel bg-[#07110a]/95 border border-emerald-500/20 flex flex-col gap-4 shadow-2xl animate-in fade-in slide-in-from-top-2 duration-200">
          <button
            onClick={() => scrollToSection("features")}
            className="text-left text-sm py-2 text-neutral-200 hover:text-emerald-400 transition-colors"
          >
            Neural AI & Multimodal Detection
          </button>
          <button
            onClick={() => scrollToSection("hardware")}
            className="text-left text-sm py-2 text-neutral-200 hover:text-emerald-400 transition-colors"
          >
            3D Hardware Lineup & Solar Kits
          </button>
          <button
            onClick={() => scrollToSection("terminal")}
            className="text-left text-sm py-2 text-neutral-200 hover:text-emerald-400 transition-colors flex items-center gap-2"
          >
            <Terminal className="w-4 h-4 text-emerald-400" />
            FreeForm™ Investigation Search
          </button>
          <button
            onClick={() => scrollToSection("corridors")}
            className="text-left text-sm py-2 text-neutral-200 hover:text-emerald-400 transition-colors"
          >
            Live Corridor Case Studies
          </button>
          <button
            onClick={() => scrollToSection("governance")}
            className="text-left text-sm py-2 text-neutral-200 hover:text-emerald-400 transition-colors"
          >
            Kenya ODPC Data Sovereignty
          </button>
          <button
            onClick={() => scrollToSection("pricing")}
            className="text-left text-sm py-2 text-neutral-200 hover:text-emerald-400 transition-colors"
          >
            M-Pesa Subscription & Calculator
          </button>
          <button
            onClick={() => scrollToSection("pricing")}
            className="w-full mt-2 py-2.5 rounded-xl text-center text-xs font-bold text-black bg-emerald-400 hover:bg-emerald-300 transition-colors"
          >
            Pre-Order Hardware Node ($49/mo)
          </button>
        </div>
      )}
    </header>
  );
}
