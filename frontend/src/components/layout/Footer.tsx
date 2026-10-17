// -------------------------------------------------------------------
// Copyright (c) 2026 Ved Vivek Talmaley. All Rights Reserved.
// This project and its original source code are strictly proprietary.
// Unauthorized copying, modification, distribution, or use is strictly prohibited.
// -------------------------------------------------------------------

export default function Footer() {
  return (
    <footer className="mt-16 border-t border-slate-800/80 bg-slate-950/80 py-8 px-4 text-xs">
      <div className="max-w-7xl mx-auto space-y-4">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-3 text-slate-400">
          <div className="flex items-center gap-2">
            <span className="font-bold text-white tracking-tight">QuantumLens</span>
            <span>•</span>
            <span className="text-slate-300">HSBC Q1 2026 Financial Intelligence</span>
          </div>
          <div className="flex items-center gap-4 text-[11px] text-slate-400 font-mono">
            <span>FastAPI Backend (Render)</span>
            <span>•</span>
            <span>ChromaDB Vector Store</span>
            <span>•</span>
            <span>Supabase PostgreSQL</span>
          </div>
        </div>

        {/* Official Proprietary License Notice */}
        <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-4 text-center sm:text-left flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="space-y-1">
            <div className="font-semibold text-slate-200 flex items-center gap-2 justify-center sm:justify-start">
              <span className="w-1.5 h-1.5 rounded-full bg-red-500" />
              <span>Copyright © 2026 Ved Vivek Talmaley. All Rights Reserved.</span>
            </div>
            <p className="text-[11px] text-slate-400 leading-relaxed max-w-3xl">
              This project and its original source code are strictly proprietary. Unauthorized copying, modification, distribution, or reproduction of this repository, via any medium, is strictly prohibited.
            </p>
          </div>
          <span className="shrink-0 text-[10px] uppercase font-mono font-bold tracking-wider px-2.5 py-1 rounded bg-slate-800 text-slate-300 border border-slate-700">
            Strictly Proprietary
          </span>
        </div>
      </div>
    </footer>
  );
}
