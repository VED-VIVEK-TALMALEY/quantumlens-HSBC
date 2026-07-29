# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from dataclasses import dataclass
from typing import List


@dataclass
class ExecutionPlan:
    intent: str
    metric: str | None
    agents: List[str]
    needs_llm: bool


class Planner:

    def plan(self, query: str) -> ExecutionPlan:

        q = query.lower()

        metric = None

        metrics = [
            "cet1",
            "tier1",
            "nii",
            "nfi",
            "roe",
            "assets",
            "liabilities",
            "customer accounts"
        ]

        for m in metrics:
            if m in q:
                metric = m
                break

        if "what is" in q or "define" in q or "meaning" in q:
            return ExecutionPlan(
                intent="definition",
                metric=metric,
                agents=["rag"],
                needs_llm=False
            )

        if "trend" in q or "over time" in q:
            return ExecutionPlan(
                intent="trend",
                metric=metric,
                agents=["sql", "chart"],
                needs_llm=False
            )

        if "compare" in q:
            return ExecutionPlan(
                intent="comparison",
                metric=metric,
                agents=["sql", "chart"],
                needs_llm=False
            )

        if "why" in q or "reason" in q or "explain" in q:
            return ExecutionPlan(
                intent="analysis",
                metric=metric,
                agents=["sql", "rag"],
                needs_llm=True
            )

        return ExecutionPlan(
            intent="metric_lookup",
            metric=metric,
            agents=["sql"],
            needs_llm=False
        )
if __name__ == "__main__":

    planner = Planner()

    tests = [
        "What is CET1 Ratio?",
        "Show CET1 trend",
        "Compare CET1 and Tier1",
        "Why did CET1 ratio fall?",
        "Show NII"
    ]

    for q in tests:
        print(q)
        print(planner.plan(q))
        print("-" * 50)