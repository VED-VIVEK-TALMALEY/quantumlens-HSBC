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
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

type Dataset = {
  label: string;
  data: number[];
  backgroundColor: string;
  borderColor?: string;
  borderWidth?: number;
};

type Props = {
  labels: string[];
  datasets: Dataset[];
  title?: string;
  unit?: string;
};

export default function BarChart({
  labels,
  datasets,
  title,
  unit = "$M",
}: Props) {
  const data = {
    labels,
    datasets: datasets.map((ds) => ({
      ...ds,
      borderRadius: 6,
      borderSkipped: false,
      maxBarThickness: 36,
    })),
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "top" as const,
        labels: {
          color: "#94a3b8",
          font: { family: "sans-serif", size: 12 },
          boxWidth: 12,
          usePointStyle: true,
          pointStyle: "circle",
        },
      },
      title: {
        display: !!title,
        text: title || "",
        color: "#f8fafc",
        font: { size: 14, weight: "bold" as const },
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
            return ` ${context.dataset.label}: ${val?.toLocaleString()} ${unit}`;
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
          callback: (value: any) => `${value} ${unit}`,
        },
      },
    },
  };

  return (
    <div className="h-72 w-full">
      <Bar data={data} options={options} />
    </div>
  );
}
