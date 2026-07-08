"use client";

import { useEffect, useState } from "react";
import api from "@/services/api";
import { Metric } from "@/types/metric";

export default function Home() {
    const [metrics, setMetrics] = useState<Metric[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.get("/metrics")
            .then((res) => {
                setMetrics(res.data);
                setLoading(false);
            })
            .catch((err) => {
                console.error("Failed to fetch metrics:", err);
                setLoading(false);
            });
    }, []);

    if (loading) return <div className="p-8">Loading metrics...</div>;

    console.log(metrics);

    return (
        <main className="p-8">
            <h1 className="text-2xl font-bold mb-6">Financial Metrics</h1>
            <div className="grid gap-4">
                {metrics.map((m) => (
                    <div key={m.metric_id} className="p-4 border rounded shadow-sm">
                        <span className="font-bold">{m.abbreviation}</span>: {m.metric_name}
                    </div>
                ))}
            </div>
        </main>
    );
}