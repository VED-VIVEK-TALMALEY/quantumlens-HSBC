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

        METRIC_ALIASES = {
            "cet1": [
                "cet1",
                "cet1 ratio",
                "common equity tier 1",
                "common equity tier 1 ratio",
                "common equity capital"
            ],
            "tier1": [
                "tier1",
                "tier 1",
                "tier1 ratio",
                "tier 1 ratio",
                "tier one"
            ],
            "nii": [
                "nii",
                "net interest income"
            ],
            "nfi": [
                "nfi",
                "net fee income",
                "net fee revenue"
            ],
            "revenue": [
                "revenue",
                "income",
                "total revenue"
            ],
            "profit_before_tax": [
                "profit before tax",
                "pbt",
                "pre tax profit"
            ],
            "assets": [
                "assets",
                "total assets"
            ],
            "liabilities": [
                "liabilities",
                "total liabilities"
            ],
            "customer_accounts": [
                "customer accounts",
                "deposits",
                "customer deposits"
            ],
            "loans": [
                "loans",
                "gross loans",
                "advances"
            ],
            "rote": [
                "rote",
                "return on tangible equity"
            ],
            "ecl": [
                "ecl",
                "expected credit loss",
                "expected credit losses"
            ]
        }

        for canonical_metric, aliases in METRIC_ALIASES.items():
            for alias in aliases:
                if alias in q:
                    metric = canonical_metric
                    break
            if metric:
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
                    ExecutionStep("financial_reasoning"),
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
                    ExecutionStep("financial_reasoning"),
                    ExecutionStep("chart")
                ],
                needs_llm=False
            )

        # -------------------------------------------------------
        # Analysis
        # -------------------------------------------------------

        if (
            "why" in q
            or "reason" in q
            or "explain" in q
        ):
            return ExecutionPlan(
                intent="analysis",
                metric=metric,
                steps=[
                    ExecutionStep("sql"),
                    ExecutionStep("audit"),
                    ExecutionStep("financial_reasoning"),
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
                    ExecutionStep("audit"),
                    ExecutionStep("financial_reasoning")
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
                ExecutionStep("financial_reasoning"),
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

    "Show CET1",

    "Show CET1 Ratio",

    "Show Common Equity Tier 1",

    "Show Common Equity Tier 1 Ratio",

    "Show Tier 1",

    "Show Tier 1 Ratio",

    "Show Net Interest Income",

    "Show NII",

    "Show Revenue",

    "Show Profit Before Tax",

    "Show Expected Credit Loss",

]

    for q in tests:
        print("=" * 60)
        print(q)
        print(planner.plan(q))