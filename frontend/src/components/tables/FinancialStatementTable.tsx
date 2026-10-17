// -------------------------------------------------------------------
// Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
// This project and its source code are strictly proprietary.
// Unauthorized copying, distribution, or use is strictly prohibited.
// -------------------------------------------------------------------

"use client";

import { useState, useMemo } from "react";

export type StatementRecord = {
  id: number;
  metric_id: number;
  metric_name: string;
  abbreviation: string;
  sheet_name: string;
  row_number: number;
  period_values?: Array<{
    period_index: number;
    period_label?: string;
    value: number;
  }>;
};

type Props = {
  records: StatementRecord[];
  selectedId: number | null;
  onSelectRecord: (record: StatementRecord) => void;
  isLoading?: boolean;
};

export default function FinancialStatementTable({
  records,
  selectedId,
  onSelectRecord,
  isLoading = false,
}: Props) {
  const [searchTerm, setSearchTerm] = useState("");
  const [statementFilter, setStatementFilter] = useState("all");
  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 12;

  // Extract unique sheet names for tabs
  const sheets = useMemo(() => {
    const set = new Set<string>();
    records.forEach((r) => {
      if (r.sheet_name) set.add(r.sheet_name);
    });
    return Array.from(set).sort();
  }, [records]);

  // Filter records
  const filteredRecords = useMemo(() => {
    return records.filter((r) => {
      const matchesSearch =
        !searchTerm ||
        r.metric_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        r.abbreviation?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        r.sheet_name?.toLowerCase().includes(searchTerm.toLowerCase());

      const matchesSheet =
        statementFilter === "all" || r.sheet_name === statementFilter;

      return matchesSearch && matchesSheet;
    });
  }, [records, searchTerm, statementFilter]);

  const totalPages = Math.ceil(filteredRecords.length / pageSize) || 1;
  const paginatedRecords = useMemo(() => {
    const start = (currentPage - 1) * pageSize;
    return filteredRecords.slice(start, start + pageSize);
  }, [filteredRecords, currentPage]);

  const getBadgeColor = (abbr: string) => {
    switch (abbr?.toLowerCase()) {
      case "pbt":
        return "bg-rose-500/20 text-rose-300 border-rose-500/30";
      case "cet1":
      case "cet1r":
        return "bg-emerald-500/20 text-emerald-300 border-emerald-500/30";
      case "nii":
        return "bg-cyan-500/20 text-cyan-300 border-cyan-500/30";
      case "rev":
        return "bg-indigo-500/20 text-indigo-300 border-indigo-500/30";
      default:
        return "bg-slate-700/40 text-slate-300 border-slate-600/40";
    }
  };

  return (
    <div className="glass-panel rounded-xl overflow-hidden border border-slate-800">
      {/* Table Header and Filters */}
      <div className="p-5 border-b border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <span>HSBC Canonical Financial Statements Table</span>
            <span className="text-xs font-medium px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
              {filteredRecords.length} Items
            </span>
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Verified Q1 2026 data pack records with PBT & key banking ratios
          </p>
        </div>

        {/* Search Input */}
        <div className="relative w-full md:w-72">
          <input
            type="text"
            placeholder="Search metric or code..."
            value={searchTerm}
            onChange={(e) => {
              setSearchTerm(e.target.value);
              setCurrentPage(1);
            }}
            className="w-full bg-slate-950/80 border border-slate-700/80 rounded-lg px-3.5 py-2 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-red-500 transition-colors"
          />
          {searchTerm && (
            <button
              onClick={() => setSearchTerm("")}
              className="absolute right-2.5 top-2 text-slate-400 hover:text-white text-xs"
            >
              ×
            </button>
          )}
        </div>
      </div>

      {/* Sheet Filter Pills */}
      <div className="px-5 py-3 border-b border-slate-800/80 bg-slate-950/40 flex items-center gap-2 overflow-x-auto text-xs">
        <span className="text-slate-500 font-medium whitespace-nowrap">
          Statement:
        </span>
        <button
          onClick={() => {
            setStatementFilter("all");
            setCurrentPage(1);
          }}
          className={`px-3 py-1 rounded-md transition-colors whitespace-nowrap ${
            statementFilter === "all"
              ? "bg-red-600 text-white font-semibold shadow-sm"
              : "bg-slate-800/60 text-slate-400 hover:text-slate-200 hover:bg-slate-800"
          }`}
        >
          All Statements ({records.length})
        </button>
        {sheets.map((sheet) => (
          <button
            key={sheet}
            onClick={() => {
              setStatementFilter(sheet);
              setCurrentPage(1);
            }}
            className={`px-3 py-1 rounded-md transition-colors whitespace-nowrap ${
              statementFilter === sheet
                ? "bg-red-600 text-white font-semibold shadow-sm"
                : "bg-slate-800/60 text-slate-400 hover:text-slate-200 hover:bg-slate-800"
            }`}
          >
            {sheet}
          </button>
        ))}
      </div>

      {/* Table Content */}
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-950/70 text-slate-400 uppercase tracking-wider font-semibold border-b border-slate-800 text-[11px]">
            <tr>
              <th className="py-3 px-4">Metric & Code</th>
              <th className="py-3 px-4">Financial Statement</th>
              <th className="py-3 px-4 text-center">Row</th>
              <th className="py-3 px-4 text-right">Latest (P1)</th>
              <th className="py-3 px-4 text-right">Prior (P2)</th>
              <th className="py-3 px-4 text-right">5-Period Trend</th>
              <th className="py-3 px-4 text-center">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {isLoading ? (
              <tr>
                <td colSpan={7} className="py-12 text-center text-slate-400">
                  <div className="inline-block animate-spin h-5 w-5 border-2 border-red-500 border-t-transparent rounded-full mr-2 align-middle"></div>
                  Loading financial records from Supabase...
                </td>
              </tr>
            ) : paginatedRecords.length === 0 ? (
              <tr>
                <td colSpan={7} className="py-8 text-center text-slate-500">
                  No statement items found matching "{searchTerm}".
                </td>
              </tr>
            ) : (
              paginatedRecords.map((r) => {
                const isSelected = selectedId === r.id;
                const p1 = r.period_values?.find((p) => p.period_index === 1);
                const p2 = r.period_values?.find((p) => p.period_index === 2);
                const p1Val = p1?.value;
                const p2Val = p2?.value;
                const hasVariance = p1Val !== undefined && p2Val !== undefined;
                const variance = hasVariance ? p1Val - p2Val : 0;
                const variancePct =
                  hasVariance && p2Val !== 0 ? (variance / Math.abs(p2Val)) * 100 : 0;

                return (
                  <tr
                    key={r.id}
                    onClick={() => onSelectRecord(r)}
                    className={`cursor-pointer transition-colors ${
                      isSelected
                        ? "bg-red-500/10 border-l-2 border-red-500"
                        : "hover:bg-slate-800/40"
                    }`}
                  >
                    <td className="py-3 px-4 font-medium text-slate-100 flex items-center gap-2">
                      <span
                        className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase border ${getBadgeColor(
                          r.abbreviation
                        )}`}
                      >
                        {r.abbreviation || "KPI"}
                      </span>
                      <span className="capitalize text-slate-200">
                        {r.metric_name?.replaceAll("_", " ")}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-slate-400">
                      {r.sheet_name}
                    </td>
                    <td className="py-3 px-4 text-center font-mono text-slate-400">
                      {r.row_number}
                    </td>
                    <td className="py-3 px-4 text-right font-mono font-semibold text-white">
                      {p1Val !== undefined ? p1Val.toLocaleString() : "—"}
                    </td>
                    <td className="py-3 px-4 text-right font-mono text-slate-400">
                      {p2Val !== undefined ? p2Val.toLocaleString() : "—"}
                    </td>
                    <td className="py-3 px-4 text-right">
                      {hasVariance ? (
                        <span
                          className={`inline-flex items-center gap-1 font-mono font-medium text-[11px] ${
                            variance >= 0 ? "text-emerald-400" : "text-rose-400"
                          }`}
                        >
                          {variance >= 0 ? "▲ +" : "▼ "}
                          {variancePct.toFixed(1)}%
                        </span>
                      ) : (
                        <span className="text-slate-500">—</span>
                      )}
                    </td>
                    <td className="py-3 px-4 text-center">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          onSelectRecord(r);
                        }}
                        className={`px-2.5 py-1 rounded text-[11px] font-medium transition ${
                          isSelected
                            ? "bg-red-600 text-white"
                            : "bg-slate-800 text-slate-300 hover:bg-slate-700"
                        }`}
                      >
                        {isSelected ? "Active" : "Inspect"}
                      </button>
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination Footer */}
      <div className="p-3.5 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400 bg-slate-950/60">
        <div>
          Showing{" "}
          <span className="font-semibold text-slate-200">
            {filteredRecords.length > 0
              ? (currentPage - 1) * pageSize + 1
              : 0}
          </span>{" "}
          to{" "}
          <span className="font-semibold text-slate-200">
            {Math.min(currentPage * pageSize, filteredRecords.length)}
          </span>{" "}
          of{" "}
          <span className="font-semibold text-slate-200">
            {filteredRecords.length}
          </span>{" "}
          records
        </div>
        <div className="flex items-center gap-2">
          <button
            disabled={currentPage <= 1}
            onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
            className="px-2.5 py-1 rounded border border-slate-700 bg-slate-900 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-slate-800 text-slate-200"
          >
            Previous
          </button>
          <span className="px-2 font-mono text-slate-300">
            Page {currentPage} of {totalPages}
          </span>
          <button
            disabled={currentPage >= totalPages}
            onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
            className="px-2.5 py-1 rounded border border-slate-700 bg-slate-900 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-slate-800 text-slate-200"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
}
