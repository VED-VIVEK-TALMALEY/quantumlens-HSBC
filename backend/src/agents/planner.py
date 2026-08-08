# -------------------------------------------------------------------

# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.

#

# This project and its source code are strictly proprietary.

# Unauthorized copying, distribution, or use is strictly prohibited.

# -------------------------------------------------------------------

from dataclasses import dataclass
from typing import List

from .execution_step import ExecutionStep

# -------------------------------------------------------------------

# Execution Plan

# -------------------------------------------------------------------

@dataclass
class ExecutionPlan:
    intent: str
    metric: str | None
    steps: List[ExecutionStep]
    needs_llm: bool
    comparison_metric: str | None = None

# -------------------------------------------------------------------

class Planner:


    # ----------------------------------------------------------------
    # Metric aliases
    # ----------------------------------------------------------------

    METRIC_ALIASES = {

        # ============================================================
        # CET1 CAPITAL
        # ============================================================

        "cet1": [
            "common equity tier one capital",
            "common equity tier 1 capital",
            "cet1 capital",
        ],

        # ============================================================
        # CET1 RATIO
        # ============================================================

        "cet1_ratio": [
            "common equity tier one ratio",
            "common equity tier 1 ratio",
            "cet1 ratio",
            "cet1r",
        ],

        # ============================================================
        # TIER 1 CAPITAL
        # ============================================================

        "tier1": [
            "tier one capital",
            "tier 1 capital",
            "tier1 capital",
            "t1 capital",
            "tier one",
            "tier 1",
            "tier1",
            "t1",
        ],

        # ============================================================
        # TIER 1 RATIO
        # ============================================================

        "tier1_ratio": [
            "tier one ratio",
            "tier 1 ratio",
            "tier1 ratio",
            "t1 ratio",
            "t1r",
        ],

        # ============================================================
        # NET INTEREST INCOME
        # ============================================================

        "nii": [
            "net interest income",
            "nii",
        ],

        # ============================================================
        # NET FEE INCOME
        # ============================================================

        "nfi": [
            "net fee income",
            "net fee revenue",
            "nfi",
        ],

        # ============================================================
        # REVENUE
        # ============================================================

        "revenue": [
            "total revenue",
            "revenue",
        ],

        # ============================================================
        # PROFIT BEFORE TAX
        # ============================================================

        "profit_before_tax": [
            "profit before tax",
            "pre tax profit",
            "pbt",
        ],

        # ============================================================
        # ASSETS
        # ============================================================

        "assets": [
            "total assets",
            "assets",
        ],

        # ============================================================
        # LIABILITIES
        # ============================================================

        "liabilities": [
            "total liabilities",
            "liabilities",
        ],

        # ============================================================
        # CUSTOMER ACCOUNTS
        # ============================================================

        "customer_accounts": [
            "customer accounts",
            "customer deposits",
            "deposits",
        ],

        # ============================================================
        # LOANS
        # ============================================================

        "loans": [
            "gross loans",
            "loans",
            "advances",
        ],

        # ============================================================
        # ROTE
        # ============================================================

        "rote": [
            "return on tangible equity",
            "rote",
        ],

        # ============================================================
        # ECL
        # ============================================================

        "ecl": [
            "expected credit losses",
            "expected credit loss",
            "ecl",
        ],
    }

    # ----------------------------------------------------------------
    # Explicit metric resolver
    # ----------------------------------------------------------------

    def _resolve_metric(self, query: str) -> List[str]:

        q = query.lower().strip()

        # ============================================================
        # Special handling for CET1
        #
        # Important:
        #
        # "CET1"                  -> CET1 ratio
        # "CET1 ratio"            -> CET1 ratio
        # "CET1 capital"          -> CET1 capital
        # ============================================================

        # ------------------------------------------------------------
        # Explicit CET1 CAPITAL
        # ------------------------------------------------------------

        if (
            "common equity tier one capital" in q
            or "common equity tier 1 capital" in q
            or "cet1 capital" in q
        ):

            matches = ["cet1"]

            # Check if comparison contains Tier 1.
            tier_metric = self._resolve_tier1_metric(q)

            if tier_metric is not None:
                matches.append(tier_metric)

            return matches

        # ------------------------------------------------------------
        # Explicit CET1 RATIO
        # ------------------------------------------------------------

        if (
            "common equity tier one ratio" in q
            or "common equity tier 1 ratio" in q
            or "cet1 ratio" in q
            or "cet1r" in q
        ):

            matches = ["cet1_ratio"]

            tier_metric = self._resolve_tier1_metric(q)

            if tier_metric is not None:
                matches.append(tier_metric)

            return matches

        # ------------------------------------------------------------
        # Bare CET1
        #
        # QuantumLens convention:
        #
        # "CET1" = CET1 ratio
        #
        # This prevents the system from accidentally querying
        # CET1 capital when the user is asking about the commonly
        # reported CET1 percentage.
        # ------------------------------------------------------------

        if "cet1" in q:

            matches = ["cet1_ratio"]

            tier_metric = self._resolve_tier1_metric(q)

            if tier_metric is not None:
                matches.append(tier_metric)

            return matches

        # ============================================================
        # Generic metric resolution
        # ============================================================

        candidates = []

        for canonical_metric, aliases in self.METRIC_ALIASES.items():

            for alias in aliases:

                position = q.find(alias)

                if position != -1:

                    candidates.append(
                        (
                            position,
                            -len(alias),
                            canonical_metric,
                        )
                    )

        # ------------------------------------------------------------
        # Sort by:
        #
        # 1. Position in query
        # 2. Longest alias at same position
        #
        # Example:
        #
        # "Compare NII with Revenue"
        #
        # NII appears first.
        # Revenue appears second.
        # ------------------------------------------------------------

        candidates.sort(
            key=lambda item: (
                item[0],
                item[1],
            )
        )

        matches = []

        for _, _, canonical_metric in candidates:

            if canonical_metric not in matches:

                matches.append(canonical_metric)

        return matches

    # ----------------------------------------------------------------
    # Tier 1 resolver
    # ----------------------------------------------------------------

    def _resolve_tier1_metric(self, query: str) -> str | None:

        q = query.lower().strip()

        # ------------------------------------------------------------
        # Explicit Tier 1 ratio
        # ------------------------------------------------------------

        if (
            "tier one ratio" in q
            or "tier 1 ratio" in q
            or "tier1 ratio" in q
            or "t1 ratio" in q
            or "t1r" in q
        ):

            return "tier1_ratio"

        # ------------------------------------------------------------
        # Explicit Tier 1 capital
        # ------------------------------------------------------------

        if (
            "tier one capital" in q
            or "tier 1 capital" in q
            or "tier1 capital" in q
            or "t1 capital" in q
        ):

            return "tier1"

        # ------------------------------------------------------------
        # Bare Tier 1
        #
        # "Tier 1" is interpreted as Tier 1 capital.
        # ------------------------------------------------------------

        if (
            "tier one" in q
            or "tier 1" in q
            or "tier1" in q
            or "t1" in q
        ):

            return "tier1"

        return None

    # ----------------------------------------------------------------
    # Intent helpers
    # ----------------------------------------------------------------

    def _is_comparison(self, query: str, metrics: List[str]) -> bool:

        q = query.lower()

        if len(metrics) < 2:
            return False

        return (
            "compare" in q
            or "comparison" in q
            or "versus" in q
            or " vs " in q
            or " vs." in q
            or "with" in q
        )

    # ----------------------------------------------------------------

    def _is_analysis(self, query: str) -> bool:

        q = query.lower()

        return (
            "why" in q
            or "reason" in q
            or "cause" in q
            or "caused" in q
            or "driver" in q
            or "drivers" in q
            or "impact" in q
            or "fall" in q
            or "fell" in q
            or "drop" in q
            or "dropped" in q
            or "decline" in q
            or "decrease" in q
            or "decreased" in q
            or "increase" in q
            or "increased" in q
            or "rise" in q
            or "rose" in q
            or "grew" in q
            or "growth" in q
        )

    # ----------------------------------------------------------------

    def _is_definition(self, query: str) -> bool:

        q = query.lower()

        return (
            "what is" in q
            or "what are" in q
            or "define" in q
            or "definition" in q
            or "meaning" in q
            or (
                "explain" in q
                and not self._is_analysis(query)
            )
        )

    # ----------------------------------------------------------------

    def _is_trend(self, query: str) -> bool:

        q = query.lower()

        return (
            "trend" in q
            or "over time" in q
            or "historical" in q
            or "history" in q
            or "historically" in q
        )

    # ----------------------------------------------------------------
    # Main planning function
    # ----------------------------------------------------------------

    def plan(self, query: str) -> ExecutionPlan:

        q = query.lower().strip()

        metrics = self._resolve_metric(query)

        metric = (
            metrics[0]
            if metrics
            else None
        )

        comparison_metric = (
            metrics[1]
            if len(metrics) > 1
            else None
        )

        # ============================================================
        # 1. COMPARISON
        # ============================================================

        if self._is_comparison(query, metrics):

            return ExecutionPlan(
                intent="comparison",
                metric=metric,
                comparison_metric=comparison_metric,
                steps=[
                    ExecutionStep("sql"),
                    ExecutionStep("audit"),
                    ExecutionStep("financial_reasoning"),
                    ExecutionStep("chart"),
                ],
                needs_llm=False,
            )

        # ============================================================
        # 2. ANALYSIS
        # ============================================================

        if self._is_analysis(query):

            return ExecutionPlan(
                intent="analysis",
                metric=metric,
                comparison_metric=None,
                steps=[
                    ExecutionStep("sql"),
                    ExecutionStep("audit"),
                    ExecutionStep("financial_reasoning"),
                    ExecutionStep("rag"),
                    ExecutionStep("llm"),
                ],
                needs_llm=True,
            )

        # ============================================================
        # 3. DEFINITION
        # ============================================================

        if self._is_definition(query):

            return ExecutionPlan(
                intent="definition",
                metric=metric,
                comparison_metric=None,
                steps=[
                    ExecutionStep("rag"),
                ],
                needs_llm=False,
            )

        # ============================================================
        # 4. TREND
        # ============================================================

        if self._is_trend(query):

            return ExecutionPlan(
                intent="trend",
                metric=metric,
                comparison_metric=None,
                steps=[
                    ExecutionStep("sql"),
                    ExecutionStep("audit"),
                    ExecutionStep("financial_reasoning"),
                    ExecutionStep("chart"),
                ],
                needs_llm=False,
            )

        # ============================================================
        # 5. METRIC LOOKUP
        # ============================================================

        if metric is not None:

            return ExecutionPlan(
                intent="metric_lookup",
                metric=metric,
                comparison_metric=None,
                steps=[
                    ExecutionStep("sql"),
                    ExecutionStep("audit"),
                    ExecutionStep("financial_reasoning"),
                ],
                needs_llm=False,
            )

        # ============================================================
        # 6. DEFAULT ANALYSIS
        # ============================================================

        # -------------------------------------------------------
# General / Company-level analysis
# -------------------------------------------------------

        return ExecutionPlan(
            intent="general_analysis",
            metric=None,
            comparison_metric=None,
            steps=[
                ExecutionStep("rag"),
                ExecutionStep("llm"),
            ],
            needs_llm=True,
        )

# -------------------------------------------------------------------

# Testing

# -------------------------------------------------------------------

if __name__ == "__main__":


    planner = Planner()

    tests = [

    # ============================================================
    # 1. BASIC METRIC LOOKUPS
    # ============================================================

    "Show CET1",
    "Show CET1 capital",
    "Show CET1 ratio",
    "Show Tier 1",
    "Show Tier 1 capital",
    "Show Tier 1 ratio",
    "Show NII",
    "Show NFI",
    "Show revenue",
    "Show PBT",
    "Show assets",
    "Show liabilities",
    "Show deposits",
    "Show loans",
    "Show RoTE",
    "Show ECL",

    # ============================================================
    # 2. DEFINITIONS
    # ============================================================

    "What is CET1?",
    "What is CET1 ratio?",
    "What is Tier 1?",
    "What is Tier 1 ratio?",
    "What is NII?",
    "What is NFI?",
    "What is RoTE?",
    "What is ECL?",
    "Define CET1",
    "Define NII",
    "Explain CET1",
    "Explain Tier 1 ratio",

    # ============================================================
    # 3. TRENDS
    # ============================================================

    "Show CET1 trend",
    "Show CET1 capital trend",
    "Show CET1 ratio trend",
    "Show Tier 1 trend",
    "Show Tier 1 ratio trend",
    "Show NII trend",
    "Show revenue trend",
    "Show PBT trend",
    "Show ECL trend",

    "Show CET1 over time",
    "Show NII over time",
    "Show historical revenue",
    "Show historical PBT",

    # ============================================================
    # 4. ANALYSIS / WHY
    # ============================================================

    "Why did CET1 fall?",
    "Why did CET1 ratio fall?",
    "Why did CET1 increase?",
    "Why did NII fall?",
    "Why did NII increase?",
    "Why did revenue fall?",
    "Why did revenue increase?",
    "Why did PBT decline?",

    "What caused the CET1 decline?",
    "What caused the NII increase?",
    "What drove the revenue increase?",
    "What was the impact on CET1?",
    "Explain the fall in CET1",
    "Explain the increase in NII",

    # ============================================================
    # 5. COMPARISONS
    # ============================================================

    "Compare CET1 with Tier 1",
    "Compare CET1 ratio with Tier 1 ratio",
    "Compare CET1 versus Tier 1",
    "Compare Tier 1 with CET1",

    "Compare NII with Revenue",
    "Compare Revenue with NII",
    "Compare NII versus Revenue",
    "Compare Revenue versus NII",

    "Compare CET1 capital with CET1 ratio",

    # ============================================================
    # 6. NATURAL LANGUAGE
    # ============================================================

    "How is CET1 performing?",
    "How is NII performing?",
    "How is HSBC performing?",
    "What happened to HSBC?",
    "What happened to HSBC in Q1 2026?",
    "Give me an overview of HSBC",
    "Give me a financial overview",
    "Summarize HSBC's financial performance",

    # ============================================================
    # 7. CASE / FORMATTING ROBUSTNESS
    # ============================================================

    "show cet1",
    "SHOW CET1",
    "Show Cet1",
    "show nii",
    "SHOW REVENUE",

    # ============================================================
    # 8. NO METRIC
    # ============================================================

    "What happened?",
    "Give me an analysis",
    "Analyze the financial results",
    "Explain the financial performance",
    "Give me an overview",

]
   

    for q in tests:

        plan = planner.plan(q)

        print("=" * 80)
        print(f"QUERY:       {q}")
        print(f"INTENT:      {plan.intent}")
        print(f"METRIC:      {plan.metric}")
        print(f"COMPARISON:  {plan.comparison_metric}")
        print(
            f"STEPS:       {[step.agent for step in plan.steps]}"
        )
        print(f"NEEDS LLM:   {plan.needs_llm}")