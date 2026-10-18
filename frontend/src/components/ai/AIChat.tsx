// -------------------------------------------------------------------
// Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
// This project and its source code are strictly proprietary.
// Unauthorized copying, distribution, or use is strictly prohibited.
// -------------------------------------------------------------------

"use client";

import { useState } from "react";
import api from "@/services/api";

type Props = {
  activeMetricName?: string;
};

interface OrchestratorResponse {
  status?: string;
  intent?: string;
  metric?: string;
  answer?: string;
  confidence?: number;
  warnings?: string[];
  evidence?: string;
  page?: number | string | null;
  financial_reasoning?: string;
  conversation_id?: string;
}

export default function AIChat({ activeMetricName }: Props) {
  const [question, setQuestion] = useState("");
  const [conversationId, setConversationId] = useState<string>(() => {
    if (typeof crypto !== "undefined" && crypto.randomUUID) {
      return crypto.randomUUID();
    }
    return `session-${Date.now()}`;
  });
  const [history, setHistory] = useState<Array<{ q: string; response: OrchestratorResponse }>>([]);
  const [loading, setLoading] = useState(false);
  const [queryTime, setQueryTime] = useState<string | null>(null);
  const [errorDetails, setErrorDetails] = useState<string | null>(null);

  const samplePrompts = [
    "Analyze HSBC Q1 2026 Profit Before Tax (PBT)",
    "Why did CET1 ratio fall from 14.8% to 14.0%?",
    "Summarize Net Interest Income (NII) performance across periods",
    "Compare Operating Expenses with Core Revenue",
  ];

  const handleAsk = async (promptToUse?: string) => {
    const q = (promptToUse || question).trim();
    if (!q || loading) return;

    if (promptToUse) {
      setQuestion(promptToUse);
    }

    setLoading(true);
    setErrorDetails(null);
    const startTime = Date.now();

    try {
      // Connect to the multi-agent orchestrator route (/query)
      const res = await api.post(
        "/query",
        {
          question: q,
          conversation_id: conversationId,
        },
        { timeout: 30000 }
      );

      const elapsed = ((Date.now() - startTime) / 1000).toFixed(2);
      setQueryTime(`${elapsed}s`);

      const data: OrchestratorResponse = res.data || {};
      if (data.conversation_id) {
        setConversationId(data.conversation_id);
      }

      setHistory((prev) => [...prev, { q, response: data }]);
      setQuestion("");
    } catch (err: any) {
      const elapsed = ((Date.now() - startTime) / 1000).toFixed(2);
      setQueryTime(`${elapsed}s`);
      console.warn("AI /query error:", err?.message);

      // P0 FIX: Never invent fake analysis on backend failure.
      // Display explicit "Live Analysis Unavailable" error state.
      const reason = err?.response?.data?.detail || err?.message || "Service connection timed out";
      setErrorDetails(reason);
    } finally {
      setLoading(false);
    }
  };

  const handleResetConversation = () => {
    const newId = typeof crypto !== "undefined" && crypto.randomUUID ? crypto.randomUUID() : `session-${Date.now()}`;
    setConversationId(newId);
    setHistory([]);
    setErrorDetails(null);
    setQueryTime(null);
  };

  return (
    <div className="glass-panel rounded-xl p-5 border border-slate-800">
      <div className="flex items-center justify-between mb-3 pb-3 border-b border-slate-800">
        <div className="flex items-center gap-2.5">
          <div className="w-7 h-7 rounded-lg bg-red-600/20 border border-red-500/40 flex items-center justify-center text-red-500 font-bold text-xs">
            AI
          </div>
          <div>
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <span>QuantumLens Multi-Agent Orchestrator</span>
              <span className="px-1.5 py-0.5 rounded text-[10px] font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                SQL • Audit • Reasoning • RAG
              </span>
            </h3>
            <p className="text-[11px] text-slate-400">
              Full multi-agent financial intelligence with conversational context tracking
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          {history.length > 0 && (
            <button
              onClick={handleResetConversation}
              className="text-[10px] px-2 py-0.5 rounded bg-slate-800/80 hover:bg-slate-700 text-slate-300 border border-slate-700 transition"
              title="Reset conversational context memory"
            >
              New Thread
            </button>
          )}
          {queryTime && (
            <span className="text-[11px] font-mono text-slate-400 bg-slate-900 px-2 py-0.5 rounded border border-slate-800">
              Latency: {queryTime}
            </span>
          )}
        </div>
      </div>

      {/* Quick Prompt Pills */}
      <div className="mb-3.5 flex flex-wrap gap-1.5">
        {samplePrompts.map((prompt, idx) => (
          <button
            key={idx}
            disabled={loading}
            onClick={() => handleAsk(prompt)}
            className="text-[11px] px-2.5 py-1 rounded-md bg-slate-800/70 hover:bg-slate-700/80 text-slate-300 hover:text-white border border-slate-700/60 transition disabled:opacity-50 text-left"
          >
            {prompt}
          </button>
        ))}
      </div>

      {/* Query Input */}
      <div className="flex gap-2">
        <input
          type="text"
          value={question}
          disabled={loading}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !loading) {
              handleAsk();
            }
          }}
          placeholder="Ask a question about HSBC Q1 2026 financial metrics (or follow up)..."
          className="flex-1 bg-slate-950/90 border border-slate-700 rounded-lg px-3.5 py-2 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-red-500 transition-colors disabled:opacity-50"
        />
        <button
          onClick={() => handleAsk()}
          disabled={loading || !question.trim()}
          className="px-4 py-2 bg-red-600 hover:bg-red-500 text-white font-semibold rounded-lg text-xs transition disabled:opacity-40 disabled:cursor-not-allowed flex items-center gap-1.5 shadow-sm"
        >
          {loading ? (
            <>
              <div className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin" />
              <span>Orchestrating...</span>
            </>
          ) : (
            <span>Ask Analyst</span>
          )}
        </button>
      </div>

      {/* Error / Live Analysis Unavailable State */}
      {errorDetails && (
        <div className="mt-4 p-4 rounded-lg bg-red-950/30 border border-red-500/40 text-xs text-red-200">
          <div className="flex items-center gap-2 font-semibold text-red-400 mb-1">
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <span>Live Analysis Unavailable</span>
          </div>
          <p className="text-[11px] text-slate-300 mb-2">
            The multi-agent orchestrator (/query) did not return a live response. Fallback financial analysis is deliberately disabled to protect data integrity.
          </p>
          <div className="p-2 bg-slate-950/80 rounded border border-red-900/40 font-mono text-[10px] text-red-300">
            Error: {errorDetails}
          </div>
        </div>
      )}

      {/* Conversation Thread History */}
      {history.length > 0 && (
        <div className="mt-4 space-y-3 max-h-[460px] overflow-y-auto pr-1">
          {history.map((item, idx) => {
            const resp = item.response;
            const answerText =
              resp.answer ||
              (resp as any).definition ||
              (resp as any).summary ||
              (typeof resp === "string" ? resp : JSON.stringify(resp, null, 2));

            return (
              <div key={idx} className="p-3.5 rounded-lg bg-slate-950/80 border border-slate-800 text-xs text-slate-200 space-y-2">
                <div className="flex items-center justify-between text-[11px] text-slate-400 pb-2 border-b border-slate-800/80">
                  <span className="font-semibold text-slate-300 flex items-center gap-1.5">
                    <span className="text-red-400 font-bold">Q:</span> {item.q}
                  </span>
                  {resp.confidence !== undefined && (
                    <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                      Audit Confidence: {(resp.confidence * 100).toFixed(0)}%
                    </span>
                  )}
                </div>

                {/* Main Answer */}
                <div className="leading-relaxed whitespace-pre-wrap text-slate-100">
                  {answerText}
                </div>

                {/* Audit Warnings if any */}
                {resp.warnings && resp.warnings.length > 0 && (
                  <div className="p-2 rounded bg-amber-500/10 border border-amber-500/30 text-[11px] text-amber-300">
                    <span className="font-semibold">Auditor Warning:</span> {resp.warnings.join(", ")}
                  </div>
                )}

                {/* Documentary Citations */}
                {resp.page && (
                  <div className="text-[10px] text-slate-400 flex items-center gap-1 pt-1 border-t border-slate-900">
                    <span className="font-semibold text-slate-300">Verified Source:</span> HSBC Q1 2026 Earnings Release (Page {resp.page})
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}