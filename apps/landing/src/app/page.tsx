"use client";

import React from "react";
import { Navbar } from "@/components/Navbar";
import { Hero } from "@/components/Hero";
import { GovernanceBar } from "@/components/GovernanceBar";
import { PartnersMarquee } from "@/components/PartnersMarquee";
import { BentoFeatures } from "@/components/BentoFeatures";
import { HardwareFlipCards } from "@/components/HardwareFlipCards";
import { InteractiveTerminal } from "@/components/InteractiveTerminal";
import { CorridorCaseStudies } from "@/components/CorridorCaseStudies";
import { ImpactCounters } from "@/components/ImpactCounters";
import { WaitlistPricing } from "@/components/WaitlistPricing";
import { Footer } from "@/components/Footer";

export default function Home() {
  return (
    <main className="overflow-x-hidden w-full max-w-full min-h-screen bg-[#060b08] text-[#f2f7f4]">
      {/* Global Navigation Bar */}
      <Navbar />

      {/* Hero Section (Cinematic Center Architecture) */}
      <Hero />

      {/* 5-Pillar Data Sovereignty & Governance Bar (Dated August 14, 2026) */}
      <GovernanceBar />

      {/* Trusted Partners & SACCOs Infinite Marquee */}
      <PartnersMarquee />

      {/* Multimodal African Transit Forensics Bento Grid (Gapless Dense Grid) */}
      <BentoFeatures />

      {/* 3D Physical Hardware Lineup Flip Cards (Studio Cutout <-> Mounted Street Pole) */}
      <HardwareFlipCards />

      {/* FreeForm™ Natural Language Crime Investigation Terminal (Gemini 3.7 Flash) */}
      <InteractiveTerminal />

      {/* Location-Pinned Dispatch Corridor Case Studies & WhatsApp Broadcasts */}
      <CorridorCaseStudies />

      {/* Oversized Gradient-Blur Impact Counters */}
      <ImpactCounters />

      {/* Automated M-Pesa Micro-Subscription Waitlist Calculator & Form */}
      <WaitlistPricing />

      {/* Editorial Footer */}
      <Footer />
    </main>
  );
}
