"use client";

import { useEffect, useState } from "react";
import api from "@/services/api";
import { Metric } from "@/types/metric";
import LineChart from "@/components/charts/LineChart";
import SummaryCard from "@/components/dashboard/SummaryCard";
 import AIChat from "@/components/ai/AIChat";

export default function Home() {
    const [metrics, setMetrics] = useState<Metric[]>([]);
    const [loading, setLoading] = useState(true);

    const [records, setRecords] = useState<any[]>([]);
    const [selectedMetric, setSelectedMetric] = useState<number | null>(null);

    const [recordDetails, setRecordDetails] = useState<any | null>(null);
   
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

    const handleMetricClick = async (metricId: number) => {

        setSelectedMetric(metricId);
        setRecordDetails(null);

        try {

            const res = await api.get(`/metric/${metricId}`);

            setRecords(res.data);

        } catch (err) {

            console.error(err);

            setRecords([]);
            setRecordDetails(null);

        }
    };

    const handleRecordClick = async (recordId: number) => {

        try {

            const res = await api.get(`/record/${recordId}`);

            setRecordDetails(res.data[0]);

        } catch (err) {

            console.error(err);

        }
    };

    if (loading) {
        return (
            <div className="p-8">
                Loading metrics...
            </div>
        );
    }

    return (

        <main className="min-h-screen bg-blue-900 p-6">

            {/* Header */}

            <div className="mb-8">

                <h1 className="text-4xl font-bold">
                    QuantumLens
                </h1>

                <p className="text-black mt-2">
                    HSBC Financial Analytics Platform
                </p>

            </div>

            {/* Dashboard */}
            <div className="grid grid-cols-4 gap-4 mb-6">

    <SummaryCard
        title="Metrics"
        value={metrics.length}
    />

    <SummaryCard
        title="Records"
        value={records.length}
    />

    <SummaryCard
        title="Selected"
        value={
            recordDetails
                ? recordDetails.metric_name
                : "-"
        }
    />

    <SummaryCard
        title="Workbook"
        value={
            recordDetails
                ? "HSBC Q1 2026"
                : "-"
        }
    />

</div>

            <div className="grid grid-cols-12 gap-6">

                {/* Metrics */}

                <div className="col-span-3 bg-white rounded-xl shadow p-4 max-h-[75vh] overflow-y-auto">

                    <h2 className="text-xl font-bold mb-4">
                        Metrics
                    </h2>

                    <div className="grid gap-3">

                        {metrics.map((m) => (

                            <div
                                key={m.metric_id}
                                onClick={() => handleMetricClick(m.metric_id)}
                                className={`p-3 border rounded cursor-pointer transition ${
                                    selectedMetric === m.metric_id
                                        ? "bg-yellow-200 border-yellow-500"
                                        : "hover:bg-yellow-100"
                                }`}
                            >

                                <div className="font-bold uppercase">
                                    {m.abbreviation}
                                </div>

                                <div className="text-sm text-blue-600">
                                    {m.metric_name}
                                </div>

                            </div>

                        ))}

                    </div>

                </div>

                {/* Records */}

                <div className="col-span-3 bg-white rounded-xl shadow p-4 max-h-[75vh] overflow-y-auto">

                    <h2 className="text-xl font-bold mb-4">
                        Records
                    </h2>

                    <div className="grid gap-3">

                        {records.length === 0 ? (

                            <div className="text-blue-500">
                                Select a metric first.
                            </div>

                        ) : (

                            records.map((record) => (

                                <div
                                    key={record.id}
                                    onClick={() => handleRecordClick(record.id)}
                                    className={`border rounded p-3 cursor-pointer transition ${
                                        recordDetails?.id === record.id
                                            ? "bg-blue-100 border-blue-500"
                                            : "hover:bg-gray-100"
                                    }`}
                                >

                                    <div className="font-semibold">
                                        {record.sheet_name}
                                    </div>

                                    <div className="text-sm text-amber-500">
                                        Row {record.row_number}
                                    </div>

                                </div>

                            ))

                        )}

                    </div>

                </div>

                {/* Analytics */}

                <div className="col-span-6 bg-amber-100 rounded-xl shadow p-6">

                    <h2 className="text-xl font-bold mb-6">
                        Financial Analytics
                    </h2>

                    {recordDetails ? (

                        <>

                            <div className="mb-6">

                                <h3 className="text-2xl font-semibold capitalize">
                                    {recordDetails.metric_name.replaceAll("_", " ")}
                                </h3>

                                <p className="text-amber-500">
                                    {recordDetails.sheet_name}
                                </p>

                            </div>

                            <LineChart
                                title={recordDetails.metric_name}
                                periodValues={recordDetails.period_values}
                            />

                        </>

                    ) : (

                        <div className="flex items-center justify-center h-[400px] text-gray-500 text-lg">

                            Select a financial record to visualize trends.

                        </div>

                    )}

                </div>

            </div>
            <div className="mt-8">

    <AIChat />

</div>

        </main>

    );
}