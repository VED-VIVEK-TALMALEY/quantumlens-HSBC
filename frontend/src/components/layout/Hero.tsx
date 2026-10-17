// -------------------------------------------------------------------
// Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
// This project and its source code are strictly proprietary.
// Unauthorized copying, distribution, or use is strictly prohibited.
// -------------------------------------------------------------------

export default function Hero() {
  return (
    <section className="relative overflow-hidden rounded-2xl glass-panel border border-slate-800 p-6 md:p-8 mb-6">
      <div className="absolute top-0 right-0 -mr-16 -mt-16 w-64 h-64 bg-red-600/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-0 left-1/3 -mb-16 w-80 h-80 bg-indigo-600/10 rounded-full blur-3xl pointer-events-none" />

      <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-md bg-red-600/10 border border-red-500/20 text-red-400 text-xs font-semibold mb-3">
            <span>●</span>
            <span>HSBC HOLDINGS PLC • Q1 2026 FINANCIAL INTELLIGENCE</span>
          </div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-white tracking-tight">
            Executive Financial Analytics & Risk Dashboard
          </h1>
          <p className="text-xs md:text-sm text-slate-400 mt-2 max-w-2xl leading-relaxed">
            Standardized metrics warehouse for HSBC Group Income Statement, Balance Sheet,
            Capital Adequacy (CET1), and Profit Before Tax (PBT). Powered by automated KPI mapping,
            vectorized document intelligence, and multi-period financial trend tracking.
          </p>
        </div>

        <div className="flex flex-wrap md:flex-col gap-2.5 shrink-0 text-xs font-mono">
          <div className="bg-slate-950/70 border border-slate-800 rounded-lg px-3.5 py-2">
            <span className="text-slate-500 block text-[10px] uppercase font-sans">Workbook Source</span>
            <span className="text-slate-200 font-semibold">260505-1q-2026-data-pack</span>
          </div>
          <div className="bg-slate-950/70 border border-slate-800 rounded-lg px-3.5 py-2">
            <span className="text-slate-500 block text-[10px] uppercase font-sans">Primary Metric Warehouse</span>
            <span className="text-emerald-400 font-semibold">Supabase PostgreSQL (Active)</span>
          </div>
        </div>
      </div>
    </section>
  );
}
