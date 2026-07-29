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
} from "chart.js";

import { Line } from "react-chartjs-2";

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

type PeriodValue = {
    period_index: number;
    value: number;
};

type Props = {
    periodValues: PeriodValue[];
    title: string;
};

export default function LineChart({
    periodValues,
    title,
}: Props) {

    const data = {
        labels: periodValues.map((p) => `P${p.period_index}`),

        datasets: [
            {
                label: title,
                data: periodValues.map((p) => p.value),
                borderColor: "#2563eb",
                backgroundColor: "rgba(37,99,235,0.2)",
                borderWidth: 3,
                pointRadius: 5,
                pointHoverRadius: 7,
                fill: false,
                tension: 0.3,
            },
        ],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
    };

    return (
        <div className="h-80 w-full">
            <Line
                data={data}
                options={options}
            />
        </div>
    );
}