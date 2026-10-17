// -------------------------------------------------------------------
// Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
// This project and its source code are strictly proprietary.
// Unauthorized copying, distribution, or use is strictly prohibited.
// -------------------------------------------------------------------

"use client";

type PeriodValue = {
  period_index: number;
  period_label?: string;
  value: number;
};

type Props = {
  metricName: string;
  sheetName: string;
  rowNumber: number;
  periodValues: PeriodValue[];
  unit?: string;
};

export default function PeriodVarianceTable({
  metricName,
  sheetName,
  rowNumber,
  periodValues,
  unit = "$M",
}: Props) {
  if (!periodValues || periodValues.length === 0) {
    return (
      <div className="p-6 text-center text-slate-500 text-xs">
        No period history available for this record.
      </div>
    );
  }

  // Calculate variances
  const rows = periodValues.map((curr, idx) => {
    const prev = idx > 0 ? periodValues[idx - 1] : null;
    const delta = prev !== null ? curr.value - prev.value : 0;
    const deltaPct =
      prev !== null && prev.value !== 0 ? (delta / Math.abs(prev.value)) * 100 : 0;

    return {
      period: curr.period_label || `Period ${curr.period_index}`,
      index: curr.period_index,
      value: curr.value,
      hasDelta: prev !== null,
      delta,
      deltaPct,
    };
  });

  return (
    <div className="glass-panel rounded-xl overflow-hidden border border-slate-800">
      <div className="p-4 border-b border-slate-800 flex items-center justify-between bg-slate-900/60">
        <div>
          <h4 className="text-sm font-bold text-white capitalize">
            {metricName.replaceAll("_", " ")} — Variance Breakdown
          </h4>
          <p className="text-[11px] text-slate-400">
            {sheetName} (Row {rowNumber})
          </p>
        </div>
        <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
          {rows.length} Reporting Periods
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-950/70 text-slate-400 uppercase tracking-wider font-semibold border-b border-slate-800 text-[10px]">
            <tr>
              <th className="py-2.5 px-3">Period</th>
              <th className="py-2.5 px-3 text-right">Value ({unit})</th>
              <th className="py-2.5 px-3 text-right">Delta ({unit})</th>
              <th className="py-2.5 px-3 text-right">Change (%)</th>
              <th className="py-2.5 px-3 text-center">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {rows.map((row) => (
              <tr key={row.index} className="hover:bg-slate-800/30 transition-colors">
                <td className="py-2 px-3 font-medium text-slate-200">
                  {row.period}
                </td>
                <td className="py-2 px-3 text-right font-mono font-semibold text-white">
                  {row.value.toLocaleString()}
                </td>
                <td className="py-2 px-3 text-right font-mono">
                  {row.hasDelta ? (
                    <span
                      className={
                        row.delta > 0
                          ? "text-emerald-400"
                          : row.delta < 0
                          ? "text-rose-400"
                          : "text-slate-400"
                      }
                    >
                      {row.delta > 0 ? "+" : ""}
                      {row.delta.toLocaleString()}
                    </span>
                  ) : (
                    <span className="text-slate-500">—</span>
                  )}
                </td>
                <td className="py-2 px-3 text-right font-mono">
                  {row.hasDelta ? (
                    <span
                      className={`inline-block px-1.5 py-0.5 rounded text-[10px] font-semibold ${
                        row.delta > 0
                          ? "bg-emerald-500/10 text-emerald-400"
                          : row.delta < 0
                          ? "bg-rose-500/10 text-rose-400"
                          : "text-slate-400"
                      }`}
                    >
                      {row.delta > 0 ? "+" : ""}
                      {row.deltaPct.toFixed(1)}%
                    </span>
                  ) : (
                    <span className="text-slate-500">—</span>
                  )}
                </td>
                <td className="py-2 px-3 text-center">
                  {!row.hasDelta ? (
                    <span className="text-[10px] text-slate-500">Baseline</span>
                  ) : row.delta > 0 ? (
                    <span className="text-[10px] text-emerald-400 font-medium">Growth</span>
                  ) : row.delta < 0 ? (
                    <span className="text-[10px] text-rose-400 font-medium">Decline</span>
                  ) : (
                    <span className="text-[10px] text-slate-400">Stable</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
