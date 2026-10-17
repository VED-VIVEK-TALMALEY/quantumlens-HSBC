// -------------------------------------------------------------------
// Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
// This project and its source code are strictly proprietary.
// Unauthorized copying, distribution, or use is strictly prohibited.
// -------------------------------------------------------------------

"use client";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from "chart.js";
import { Line } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

type PeriodValue = {
  period_index: number;
  period_label?: string;
  value: number;
};

type Props = {
  periodValues: PeriodValue[];
  title: string;
  color?: string;
  fillColor?: string;
  unit?: string;
};

export default function LineChart({
  periodValues,
  title,
  color = "#3b82f6",
  fillColor = "rgba(59, 130, 246, 0.12)",
  unit = "$M",
}: Props) {
  if (!periodValues || periodValues.length === 0) {
    return (
      <div className="flex h-72 w-full items-center justify-center text-slate-500 text-sm">
        No period data available for this metric.
      </div>
    );
  }

  const labels = periodValues.map(
    (p) => p.period_label || `Period ${p.period_index}`
  );
  const dataPoints = periodValues.map((p) => p.value);

  const data = {
    labels,
    datasets: [
      {
        label: title.replaceAll("_", " ").toUpperCase(),
        data: dataPoints,
        borderColor: color,
        backgroundColor: fillColor,
        borderWidth: 2.5,
        pointBackgroundColor: color,
        pointBorderColor: "#0f172a",
        pointBorderWidth: 2,
        pointRadius: 4.5,
        pointHoverRadius: 7,
        pointHoverBackgroundColor: "#ffffff",
        pointHoverBorderColor: color,
        fill: true,
        tension: 0.35,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: "top" as const,
        labels: {
          color: "#cbd5e1",
          font: { family: "sans-serif", size: 12, weight: 600 },
          boxWidth: 12,
          usePointStyle: true,
          pointStyle: "circle",
        },
      },
      tooltip: {
        backgroundColor: "#0f172a",
        titleColor: "#f8fafc",
        bodyColor: "#cbd5e1",
        borderColor: "#334155",
        borderWidth: 1,
        padding: 10,
        callbacks: {
          label: (context: any) => {
            const val = context.parsed.y;
            return ` Value: ${val?.toLocaleString()} ${unit}`;
          },
        },
      },
    },
    scales: {
      x: {
        grid: { color: "rgba(51, 65, 85, 0.2)" },
        ticks: { color: "#64748b", font: { size: 11 } },
      },
      y: {
        grid: { color: "rgba(51, 65, 85, 0.2)" },
        ticks: {
          color: "#64748b",
          font: { size: 11 },
          callback: (val: any) => `${val?.toLocaleString()} ${unit}`,
        },
      },
    },
  };

  return (
    <div className="h-72 w-full">
      <Line data={data} options={options} />
    </div>
  );
}