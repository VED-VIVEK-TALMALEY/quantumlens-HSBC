"use client";

import { useState } from "react";
import api from "@/services/api";

export default function AIChat() {

    const [question, setQuestion] = useState("");

    const [answer, setAnswer] = useState("");

    const [loading, setLoading] = useState(false);

    const askAI = async () => {

        if (!question.trim()) return;

        setLoading(true);

        try {

            const res = await api.post("/ask", {
                question,
            });

            setAnswer(res.data.answer ?? JSON.stringify(res.data));

        } catch (err) {

            console.error(err);

            setAnswer("Unable to generate response.");

        }

        setLoading(false);

    };

    return (

        <div className="bg-white rounded-xl shadow p-6">

            <h2 className="text-2xl font-bold mb-4">

                 AI Financial Assistant

            </h2>

            <div className="flex gap-3">

                <input
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Ask about HSBC financial statements..."
                    className="flex-1 border rounded-lg px-4 py-3 outline-none"
                />

                <button
                    onClick={askAI}
                    className="bg-black text-white rounded-lg px-6 hover:bg-gray-800"
                >

                    Ask

                </button>

            </div>

            {loading && (

                <p className="mt-4 text-black">

                    Thinking...

                </p>

            )}

            {answer && (

                <div className="mt-6 border rounded-lg p-4 bg-gray-50 whitespace-pre-wrap">

                    {answer}

                </div>

            )}

        </div>

    );

}