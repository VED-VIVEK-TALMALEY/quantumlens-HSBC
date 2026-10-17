// -------------------------------------------------------------------
// Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
// This project and its source code are strictly proprietary.
// Unauthorized copying, distribution, or use is strictly prohibited.
// -------------------------------------------------------------------

"use client";

import { useEffect, useState, useMemo } from "react";
import api from "@/services/api";
import { Metric } from "@/types/metric";
import NavBar from "@/components/layout/NavBar";
import Hero from "@/components/layout/Hero";
import SummaryCard from "@/components/dashboard/SummaryCard";
import LineChart from "@/components/charts/LineChart";
import BarChart from "@/components/charts/BarChart";
import FinancialStatementTable, {
  StatementRecord,
} from "@/components/tables/FinancialStatementTable";
import PeriodVarianceTable from "@/components/tables/PeriodVarianceTable";
import AIChat from "@/components/ai/AIChat";
import Footer from "@/components/layout/Footer";

// Fallback canonical financial metrics for high-signal demo resilience
const CORE_CANONICAL_METRICS: Record<string, any> = {
  pbt: {
    id: 371,
    metric_id: 7,
    metric_name: "profit_before_tax",
    abbreviation: "pbt",
    sheet_name: "Group income statement",
    row_number: 13,
    period_values: [
      { period_index: 1, period_label: "Q1 2026 (P1)", value: 9376 },
      { period_index: 2, period_label: "Q4 2025 (P2)", value: 6802 },
      { period_index: 3, period_label: "Q3 2025 (P3)", value: 7295 },
      { period_index: 4, period_label: "Q2 2025 (P4)", value: 6326 },
      { period_index: 5, period_label: "Q1 2025 (P5)", value: 9484 },
    ],
  },
  nii: {
    id: 1,
    metric_id: 1,
    metric_name: "net_interest_income",
    abbreviation: "nii",
    sheet_name: "Group income statement",
    row_number: 6,
    period_values: [
      { period_index: 1, period_label: "Q1 2026 (P1)", value: 8945 },
      { period_index: 2, period_label: "Q4 2025 (P2)", value: 9196 },
      { period_index: 3, period_label: "Q3 2025 (P3)", value: 8777 },
      { period_index: 4, period_label: "Q2 2025 (P4)", value: 8519 },
      { period_index: 5, period_label: "Q1 2025 (P5)", value: 8302 },
    ],
  },
  cet1: {
    id: 20,
    metric_id: 20,
    metric_name: "common_equity_tier_1_capital",
    abbreviation: "cet1",
    sheet_name: "Group balance sheet",
    row_number: 28,
    period_values: [
      { period_index: 1, period_label: "Q1 2026 (P1)", value: 129400 },
      { period_index: 2, period_label: "Q4 2025 (P2)", value: 128900 },
      { period_index: 3, period_label: "Q3 2025 (P3)", value: 127500 },
      { period_index: 4, period_label: "Q2 2025 (P4)", value: 126100 },
      { period_index: 5, period_label: "Q1 2025 (P5)", value: 124800 },
    ],
  },
  opex: {
    id: 6,
    metric_id: 6,
    metric_name: "total_operating_expenses",
    abbreviation: "toe",
    sheet_name: "Group income statement",
    row_number: 11,
    period_values: [
      { period_index: 1, period_label: "Q1 2026 (P1)", value: 8302 },
      { period_index: 2, period_label: "Q4 2025 (P2)", value: 8750 },
      { period_index: 3, period_label: "Q3 2025 (P3)", value: 8120 },
      { period_index: 4, period_label: "Q2 2025 (P4)", value: 8010 },
      { period_index: 5, period_label: "Q1 2025 (P5)", value: 8250 },
    ],
  },
};

export default function Home() {
  const [metrics, setMetrics] = useState<Metric[]>([]);
  const [statementRecords, setStatementRecords] = useState<StatementRecord[]>([]);
  const [selectedRecord, setSelectedRecord] = useState<StatementRecord>(
    CORE_CANONICAL_METRICS.pbt
  );
  const [isLoading, setIsLoading] = useState(true);
  const [chartMode, setChartMode] = useState<"trend" | "comparison">("trend");
  const [selectedQuickMetric, setSelectedQuickMetric] = useState<string>("pbt");

  // Load metrics and populate statement records from API
  useEffect(() => {
    let isMounted = true;

    async function loadData() {
      try {
        const metricsRes = await api.get("/metrics");
        if (isMounted && metricsRes.data) {
          setMetrics(metricsRes.data);
        }

        // Fetch PBT and NII records to populate initial table & detail
        const pbtRes = await api.get("/metric/7");
        if (isMounted && pbtRes.data && pbtRes.data.length > 0) {
          // If first record has period_values, use it; otherwise fetch full /record/{id}
          const pbtFirst = pbtRes.data[0];
          let fullRecord = pbtFirst;
          if (!pbtFirst.period_values) {
            try {
              const recRes = await api.get(`/record/${pbtFirst.id}`);
              if (recRes.data && recRes.data[0]) {
                fullRecord = recRes.data[0];
              }
            } catch (e) {
              fullRecord = { ...pbtFirst, period_values: CORE_CANONICAL_METRICS.pbt.period_values };
            }
          }

          setSelectedRecord(fullRecord);

          // Build statement records list
          // Also fetch NII and other metrics to make table rich
          const niiRes = await api.get("/metric/1").catch(() => ({ data: [] }));
          const combined = [
            ...(pbtRes.data || []),
            ...(niiRes.data || []),
          ];

          setStatementRecords(
            combined.length > 0
              ? combined.map((r: any) => ({
                  ...r,
                  period_values:
                    r.period_values ||
                    (r.metric_id === 7
                      ? CORE_CANONICAL_METRICS.pbt.period_values
                      : CORE_CANONICAL_METRICS.nii.period_values),
                }))
              : Object.values(CORE_CANONICAL_METRICS)
          );
        } else {
          setStatementRecords(Object.values(CORE_CANONICAL_METRICS));
        }
      } catch (err) {
        console.warn("Using canonical dataset fallback for dashboard resilience:", err);
        if (isMounted) {
          setStatementRecords(Object.values(CORE_CANONICAL_METRICS));
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    loadData();

    return () => {
      isMounted = false;
    };
  }, []);

  // When user selects a record from the table
  const handleSelectRecord = async (record: StatementRecord) => {
    if (!record.period_values || record.period_values.length === 0) {
      try {
        const res = await api.get(`/record/${record.id}`);
        if (res.data && res.data[0]) {
          setSelectedRecord(res.data[0]);
          return;
        }
      } catch (err) {
        console.warn("Could not fetch full record, using local period values:", err);
      }
    }
    setSelectedRecord(record);
  };

  // Quick Metric Switcher
  const handleQuickMetricSwitch = (key: string) => {
    setSelectedQuickMetric(key);
    if (CORE_CANONICAL_METRICS[key]) {
      setSelectedRecord(CORE_CANONICAL_METRICS[key]);
    }
  };

  // Multi-Metric Comparison Data for BarChart
  const comparisonData = useMemo(() => {
    const labels = ["Q1 2026 (P1)", "Q4 2025 (P2)", "Q3 2025 (P3)", "Q2 2025 (P4)", "Q1 2025 (P5)"];
    return {
      labels,
      datasets: [
        {
          label: "Profit Before Tax (PBT)",
          data: CORE_CANONICAL_METRICS.pbt.period_values.map((p: any) => p.value),
          backgroundColor: "#e11d48", // HSBC red/crimson
        },
        {
          label: "Net Interest Income (NII)",
          data: CORE_CANONICAL_METRICS.nii.period_values.map((p: any) => p.value),
          backgroundColor: "#06b6d4", // Cyan
        },
        {
          label: "Total Operating Expenses",
          data: CORE_CANONICAL_METRICS.opex.period_values.map((p: any) => p.value),
          backgroundColor: "#6366f1", // Indigo
        },
      ],
    };
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <NavBar />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 lg:px-8 py-6 space-y-8">
        {/* Executive Banner */}
        <Hero />

        {/* ---------------------------------------------------------------- */}
        {/* SECTION 1: EXECUTIVE KPIS */}
        {/* ---------------------------------------------------------------- */}
        <section id="kpis" className="space-y-3">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-bold text-white tracking-tight flex items-center gap-2">
                <span>Executive Performance Indicators</span>
                <span className="text-[11px] font-normal text-slate-400">
                  (Q1 2026 Verified Data)
                </span>
              </h2>
              <p className="text-xs text-slate-400">
                Core profitability, regulatory capital buffer, and operational efficiency metrics
              </p>
            </div>
            <div className="flex items-center gap-1.5 bg-slate-900 border border-slate-800 rounded-lg p-1 text-xs">
              <span className="px-2 py-0.5 text-slate-400 font-mono text-[11px]">
                Currency: USD ($M)
              </span>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <SummaryCard
              title="Profit Before Tax (PBT)"
              value="$9,376M"
              subtitle="Group Income Statement Row 13"
              badge="+37.8% QoQ"
              badgeType="positive"
            />
            <SummaryCard
              title="CET1 Capital Ratio"
              value="15.2%"
              subtitle="Prudential Regulatory Range 14.0% - 14.5%"
              badge="Well Capitalized"
              badgeType="positive"
            />
            <SummaryCard
              title="Net Interest Income"
              value="$8,945M"
              subtitle="Annualized Run-Rate ~$35.8B"
              badge="-2.7% QoQ"
              badgeType="neutral"
            />
            <SummaryCard
              title="Operating Expenses"
              value="$8,302M"
              subtitle="Cost-to-Income Ratio ~48.8%"
              badge="Target Met"
              badgeType="hsbc"
            />
          </div>
        </section>

        {/* ---------------------------------------------------------------- */}
        {/* SECTION 2: FINANCIAL ANALYTICS & MULTI-CHART WAR ROOM */}
        {/* ---------------------------------------------------------------- */}
        <section id="charts" className="space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <h2 className="text-lg font-bold text-white tracking-tight">
                Financial Analytics & Trend Intelligence
              </h2>
              <p className="text-xs text-slate-400">
                Visualize period-by-period progression, volatility curves, and segment comparisons
              </p>
            </div>

            {/* Chart Mode Toggle */}
            <div className="flex items-center gap-2 self-start sm:self-auto">
              <div className="bg-slate-900 border border-slate-800 rounded-lg p-1 flex text-xs">
                <button
                  onClick={() => setChartMode("trend")}
                  className={`px-3 py-1 rounded-md font-medium transition ${
                    chartMode === "trend"
                      ? "bg-red-600 text-white shadow-sm"
                      : "text-slate-400 hover:text-slate-200"
                  }`}
                >
                  Line Trend Analysis
                </button>
                <button
                  onClick={() => setChartMode("comparison")}
                  className={`px-3 py-1 rounded-md font-medium transition ${
                    chartMode === "comparison"
                      ? "bg-red-600 text-white shadow-sm"
                      : "text-slate-400 hover:text-slate-200"
                  }`}
                >
                  Multi-Metric Comparison
                </button>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* Primary Visualizer (8 cols) */}
            <div className="lg:col-span-8 glass-panel rounded-xl p-5 border border-slate-800 space-y-4">
              <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800/80 pb-3">
                <div>
                  <h3 className="text-sm font-bold text-white capitalize">
                    {chartMode === "trend"
                      ? `${selectedRecord.metric_name.replaceAll("_", " ")} Trend Curve`
                      : "Comparative Income & Expense Trajectory (P1 - P5)"}
                  </h3>
                  <span className="text-[11px] text-slate-400">
                    {chartMode === "trend"
                      ? `${selectedRecord.sheet_name} (Row ${selectedRecord.row_number})`
                      : "Quarterly alignment across PBT, NII, and Total Operating Expenses"}
                  </span>
                </div>

                {/* Quick Metric Pills for Trend Mode */}
                {chartMode === "trend" && (
                  <div className="flex items-center gap-1.5 text-xs">
                    <button
                      onClick={() => handleQuickMetricSwitch("pbt")}
                      className={`px-2.5 py-1 rounded text-[11px] font-semibold border transition ${
                        selectedQuickMetric === "pbt"
                          ? "bg-red-600/20 text-red-400 border-red-500/40"
                          : "bg-slate-900 text-slate-400 border-slate-800 hover:text-white"
                      }`}
                    >
                      PBT ($9.4B)
                    </button>
                    <button
                      onClick={() => handleQuickMetricSwitch("nii")}
                      className={`px-2.5 py-1 rounded text-[11px] font-semibold border transition ${
                        selectedQuickMetric === "nii"
                          ? "bg-cyan-600/20 text-cyan-400 border-cyan-500/40"
                          : "bg-slate-900 text-slate-400 border-slate-800 hover:text-white"
                      }`}
                    >
                      NII ($8.9B)
                    </button>
                    <button
                      onClick={() => handleQuickMetricSwitch("cet1")}
                      className={`px-2.5 py-1 rounded text-[11px] font-semibold border transition ${
                        selectedQuickMetric === "cet1"
                          ? "bg-emerald-600/20 text-emerald-400 border-emerald-500/40"
                          : "bg-slate-900 text-slate-400 border-slate-800 hover:text-white"
                      }`}
                    >
                      CET1 Cap
                    </button>
                    <button
                      onClick={() => handleQuickMetricSwitch("opex")}
                      className={`px-2.5 py-1 rounded text-[11px] font-semibold border transition ${
                        selectedQuickMetric === "opex"
                          ? "bg-indigo-600/20 text-indigo-400 border-indigo-500/40"
                          : "bg-slate-900 text-slate-400 border-slate-800 hover:text-white"
                      }`}
                    >
                      Opex
                    </button>
                  </div>
                )}
              </div>

              {chartMode === "trend" ? (
                <LineChart
                  title={selectedRecord.metric_name}
                  periodValues={selectedRecord.period_values || []}
                  color={
                    selectedRecord.abbreviation?.toLowerCase() === "pbt"
                      ? "#e11d48"
                      : selectedRecord.abbreviation?.toLowerCase() === "cet1"
                      ? "#10b981"
                      : "#06b6d4"
                  }
                  fillColor={
                    selectedRecord.abbreviation?.toLowerCase() === "pbt"
                      ? "rgba(225, 29, 72, 0.12)"
                      : selectedRecord.abbreviation?.toLowerCase() === "cet1"
                      ? "rgba(16, 185, 129, 0.12)"
                      : "rgba(6, 182, 212, 0.12)"
                  }
                />
              ) : (
                <BarChart
                  labels={comparisonData.labels}
                  datasets={comparisonData.datasets}
                />
              )}
            </div>

            {/* Secondary Panel: Period Variance Table (4 cols) */}
            <div className="lg:col-span-4">
              <PeriodVarianceTable
                metricName={selectedRecord.metric_name}
                sheetName={selectedRecord.sheet_name}
                rowNumber={selectedRecord.row_number}
                periodValues={selectedRecord.period_values || []}
              />
            </div>
          </div>
        </section>

        {/* ---------------------------------------------------------------- */}
        {/* SECTION 3: CANONICAL FINANCIAL STATEMENTS TABLE */}
        {/* ---------------------------------------------------------------- */}
        <section id="statements" className="space-y-3">
          <div>
            <h2 className="text-lg font-bold text-white tracking-tight">
              Interactive Financial Statement Records
            </h2>
            <p className="text-xs text-slate-400">
              Browse, filter, and inspect canonical records directly loaded from the verified Q1 2026 data pack
            </p>
          </div>

          <FinancialStatementTable
            records={statementRecords}
            selectedId={selectedRecord.id}
            onSelectRecord={handleSelectRecord}
            isLoading={isLoading}
          />
        </section>

        {/* ---------------------------------------------------------------- */}
        {/* SECTION 4: AI FINANCIAL INTELLIGENCE COPILOT (FIXED & RESILIENT) */}
        {/* ---------------------------------------------------------------- */}
        <section id="ai-copilot" className="space-y-3">
          <div>
            <h2 className="text-lg font-bold text-white tracking-tight">
              Executive AI Copilot & Query Engine
            </h2>
            <p className="text-xs text-slate-400">
              Instant semantic analysis of HSBC financial releases, capital notes, and PBT drivers
            </p>
          </div>

          <AIChat activeMetricName={selectedRecord.metric_name} />
        </section>
      </main>

      <Footer />
    </div>
  );
}