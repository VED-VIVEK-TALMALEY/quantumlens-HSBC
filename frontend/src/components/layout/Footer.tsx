// -------------------------------------------------------------------
// Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
// This project and its source code are strictly proprietary.
// Unauthorized copying, distribution, or use is strictly prohibited.
// -------------------------------------------------------------------

export default function Footer() {
  return (
    <footer className="mt-12 py-6 border-t border-slate-800 text-slate-500 text-xs">
      <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
        <div>
          <span className="font-semibold text-slate-400">QuantumLens</span> •
          HSBC Financial Intelligence System © 2026 Ved Talmaley. Proprietary & Confidential.
        </div>
        <div className="flex items-center gap-4 text-slate-400">
          <span>FastAPI Backend (Render)</span>
          <span>•</span>
          <span>ChromaDB Vector Store</span>
          <span>•</span>
          <span>Supabase PostgreSQL</span>
        </div>
      </div>
    </footer>
  );
}
