import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Iborain Safety | Solar-Ready Edge AI Sentry & Public Safety Grid",
  description:
    "Solar-ready AI sentry grid for African transit corridors, gated estates, and commercial hubs. Real-time vehicle fingerprinting, Boda Boda classification, Gemini 3.7 Flash FreeForm search, and automated WhatsApp patrol dispatch.",
  keywords: [
    "Iborain Safety",
    "Edge AI Sentry",
    "African Transit Safety",
    "Sony IMX500",
    "Gemini 3.7 Flash",
    "Boda Boda Classification",
    "M-Pesa Micro-Subscription",
    "Kenya ODPC Compliant",
  ],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased dark`}
    >
      <body className="min-h-full flex flex-col bg-[#060b08] text-[#f2f7f4] font-sans antialiased selection:bg-emerald-500 selection:text-black">
        {children}
      </body>
    </html>
  );
}

