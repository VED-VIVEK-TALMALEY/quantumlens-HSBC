# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from dataclasses import dataclass
from typing import List
from .execution_step import ExecutionStep


@dataclass
class ExecutionPlan:
    intent: str
    metric: str | None
    steps: List[ExecutionStep]
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

        # -------------------------------------------------------
        # Definition
        # -------------------------------------------------------

        if (
            "what is" in q
            or "define" in q
            or "meaning" in q
            or (
                "explain" in q
                and (
                    "fall" not in q
                    and "increase" not in q
                    and "drop" not in q
                    and "rise" not in q
                )
            )
        ):
            return ExecutionPlan(
                intent="definition",
                metric=metric,
                steps=[
                    ExecutionStep("rag")
                ],
                needs_llm=False
            )

        # -------------------------------------------------------
        # Trend
        # -------------------------------------------------------

        if "trend" in q or "over time" in q:

            return ExecutionPlan(
                intent="trend",
                metric=metric,
                steps=[
                    ExecutionStep("sql"),
                    ExecutionStep("audit"),
                    ExecutionStep("chart")
                ],
                needs_llm=False
            )

        # -------------------------------------------------------
        # Comparison
        # -------------------------------------------------------

        if "compare" in q:

            return ExecutionPlan(
                intent="comparison",
                metric=metric,
                steps=[
                    ExecutionStep("sql"),
                    ExecutionStep("audit"),
                    ExecutionStep("chart")
                ],
                needs_llm=False
            )

        # -------------------------------------------------------
        # Analysis
        # -------------------------------------------------------

        if "why" in q or "reason" in q or "explain" in q:

            return ExecutionPlan(
                intent="analysis",
                metric=metric,
                steps=[
                    ExecutionStep("sql"),
                    ExecutionStep("audit"),
                    ExecutionStep("rag"),
                    ExecutionStep("llm")
                ],
                needs_llm=True
            )

        # -------------------------------------------------------
        # Metric Lookup
        # -------------------------------------------------------

        if metric is not None:

            return ExecutionPlan(
                intent="metric_lookup",
                metric=metric,
                steps=[
                    ExecutionStep("sql"),
                    ExecutionStep("audit")
                ],
                needs_llm=False
            )

        # -------------------------------------------------------
        # Default
        # -------------------------------------------------------

        return ExecutionPlan(
            intent="analysis",
            metric=metric,
            steps=[
                ExecutionStep("sql"),
                ExecutionStep("audit"),
                ExecutionStep("rag"),
                ExecutionStep("llm")
            ],
            needs_llm=True
        )


# -------------------------------------------------------------------
# Testing
# -------------------------------------------------------------------

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
        print("=" * 60)
        print(q)
        print(planner.plan(q))