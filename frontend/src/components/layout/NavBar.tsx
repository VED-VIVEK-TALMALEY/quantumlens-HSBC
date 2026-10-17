// -------------------------------------------------------------------
// Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
// This project and its source code are strictly proprietary.
// Unauthorized copying, distribution, or use is strictly prohibited.
// -------------------------------------------------------------------

"use client";

import Link from "next/link";

export default function NavBar() {
  return (
    <header className="sticky top-0 z-50 bg-slate-950/90 backdrop-blur-md border-b border-slate-800/80 px-4 lg:px-8 py-3">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        {/* Brand / Logo */}
        <div className="flex items-center gap-3">
          {/* HSBC Geometric Hexagon Crest */}
          <div className="relative w-7 h-7 flex items-center justify-center">
            <div className="w-6 h-6 bg-red-600 rotate-45 transform flex items-center justify-center shadow-sm shadow-red-900/50">
              <div className="w-2.5 h-2.5 bg-white transform -rotate-45" />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold text-base tracking-tight text-white">
                QuantumLens
              </span>
              <span className="px-1.5 py-0.2 rounded text-[10px] font-semibold bg-red-600/20 text-red-400 border border-red-500/30">
                HSBC Q1 2026
              </span>
            </div>
            <p className="text-[10px] text-slate-400 font-medium">
              Global Banking & Markets Intelligence
            </p>
          </div>
        </div>

        {/* Navigation Items */}
        <nav className="hidden md:flex items-center gap-6 text-xs font-medium text-slate-300">
          <a
            href="#kpis"
            className="hover:text-white transition-colors"
          >
            Executive KPIs
          </a>
          <a
            href="#charts"
            className="hover:text-white transition-colors"
          >
            Financial Analytics
          </a>
          <a
            href="#statements"
            className="hover:text-white transition-colors"
          >
            Statements Table
          </a>
          <a
            href="#ai-copilot"
            className="hover:text-white transition-colors"
          >
            AI Analyst
          </a>
        </nav>

        {/* Live System Indicator */}
        <div className="flex items-center gap-3">
          <div className="hidden sm:flex items-center gap-2 px-2.5 py-1 rounded-full bg-slate-900 border border-slate-800 text-[11px]">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-slate-300 font-mono">Live Data: 456 Records (PBT Active)</span>
          </div>
          <span className="text-xs px-2.5 py-1 rounded bg-slate-800 text-slate-300 border border-slate-700 font-mono">
            v1.0.0-Q1
          </span>
        </div>
      </div>
    </header>
  );
}
