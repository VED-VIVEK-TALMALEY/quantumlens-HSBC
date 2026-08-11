# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

import re
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
# Planner
# -------------------------------------------------------------------

class Planner:

    # ----------------------------------------------------------------
    # Metric aliases
    # ----------------------------------------------------------------

    METRIC_ALIASES = {

        # CET1 capital
        "cet1": [
            "common equity tier one capital",
            "common equity tier 1 capital",
            "cet1 capital",
        ],

        # CET1 ratio
        "cet1_ratio": [
            "common equity tier one ratio",
            "common equity tier 1 ratio",
            "cet1 ratio",
            "cet1r",
        ],

        # Tier 1 capital
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

        # Tier 1 ratio
        "tier1_ratio": [
            "tier one ratio",
            "tier 1 ratio",
            "tier1 ratio",
            "t1 ratio",
            "t1r",
        ],

        # Net interest income
        "nii": [
            "net interest income",
            "nii",
        ],

        # Net fee income
        "nfi": [
            "net fee income",
            "net fee revenue",
            "nfi",
        ],

        # Revenue
        "revenue": [
            "total revenue",
            "revenue",
        ],

        # Profit before tax
        "profit_before_tax": [
            "profit before tax",
            "pre tax profit",
            "pbt",
        ],

        # Assets
        "assets": [
            "total assets",
            "assets",
        ],

        # Liabilities
        "liabilities": [
            "total liabilities",
            "liabilities",
        ],

        # Customer accounts / deposits
        "customer_accounts": [
            "customer accounts",
            "customer deposits",
            "deposits",
        ],

        # Loans
        "loans": [
            "gross loans",
            "loans",
            "advances",
        ],

        # RoTE
        "rote": [
            "return on tangible equity",
            "rote",
        ],

        # ECL
        "ecl": [
            "expected credit losses",
            "expected credit loss",
            "ecl",
        ],
    }

    # ----------------------------------------------------------------
    # Bare metric conventions
    # ----------------------------------------------------------------

    BARE_METRIC_ALIASES = {

        # Bare CET1 means CET1 ratio.
        "cet1": "cet1_ratio",

        # Bare Tier 1 means Tier 1 capital.
        "tier one": "tier1",
        "tier 1": "tier1",
        "tier1": "tier1",
        "t1": "tier1",
    }

    # ----------------------------------------------------------------
    # Text normalization
    # ----------------------------------------------------------------

    @staticmethod
    def _normalize(text: str) -> str:
        """
        Normalize user input.

        Example:
            "Show   CET1!!!"
        becomes:
            "show cet1"
        """

        text = text.lower().strip()

        text = re.sub(r"[^a-z0-9]+", " ", text)

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    # ----------------------------------------------------------------
    # Alias matching
    # ----------------------------------------------------------------

    @staticmethod
    def _alias_match(query: str, alias: str):
        alias = Planner._normalize(alias)

        pattern = (
            rf"(?<![a-z0-9])"
            rf"{re.escape(alias)}"
            rf"(?![a-z0-9])"
        )

        return re.search(pattern, query)

    # ----------------------------------------------------------------
    # Find metric candidates
    # ----------------------------------------------------------------

    def _find_metric_candidates(self, query: str):

        candidates = []

        for canonical_metric, aliases in self.METRIC_ALIASES.items():

            for alias in aliases:

                match = self._alias_match(query, alias)

                if match:

                    candidates.append(
                        (
                            match.start(),
                            -len(alias),
                            canonical_metric,
                            alias,
                            match.start(),
                            match.end(),
                        )
                    )

        return candidates

    # ----------------------------------------------------------------
    # Resolve metric
    # ----------------------------------------------------------------

    def _resolve_metric(self, query: str) -> List[str]:

        q = self._normalize(query)

        candidates = self._find_metric_candidates(q)

        candidates.sort(
            key=lambda item: (
                item[0],
                item[1],
            )
        )

        selected = []
        occupied_ranges = []

        # ------------------------------------------------------------
        # Select longest non-overlapping explicit aliases.
        # ------------------------------------------------------------

        for candidate in candidates:

            position = candidate[0]
            canonical_metric = candidate[2]
            alias = candidate[3]
            start = candidate[4]
            end = candidate[5]

            overlaps = False

            for occupied_start, occupied_end in occupied_ranges:

                if (
                    start < occupied_end
                    and end > occupied_start
                ):
                    overlaps = True
                    break

            if overlaps:
                continue

            selected.append(
                (
                    position,
                    canonical_metric,
                    alias,
                    start,
                    end,
                )
            )

            occupied_ranges.append(
                (start, end)
            )

        # ------------------------------------------------------------
        # Mask selected explicit aliases.
        #
        # This prevents:
        #
        # "common equity tier 1 capital"
        #
        # from becoming:
        #
        # cet1 + tier1
        # ------------------------------------------------------------

        masked_query = list(q)

        for _, _, _, start, end in selected:

            for i in range(start, end):
                masked_query[i] = " "

        masked_query = "".join(masked_query)

        # ------------------------------------------------------------
        # Bare CET1 -> CET1 ratio
        # ------------------------------------------------------------

        bare_cet1_match = self._alias_match(
            masked_query,
            "cet1",
        )

        if bare_cet1_match:

            start = bare_cet1_match.start()
            end = bare_cet1_match.end()

            selected.append(
                (
                    start,
                    "cet1_ratio",
                    "cet1",
                    start,
                    end,
                )
            )

            masked_query = (
                masked_query[:start]
                + (" " * (end - start))
                + masked_query[end:]
            )

        # ------------------------------------------------------------
        # Bare Tier 1
        # ------------------------------------------------------------

        bare_tier_candidates = []

        for alias, canonical_metric in self.BARE_METRIC_ALIASES.items():

            if alias == "cet1":
                continue

            match = self._alias_match(
                masked_query,
                alias,
            )

            if match:

                bare_tier_candidates.append(
                    (
                        match.start(),
                        -len(alias),
                        canonical_metric,
                        alias,
                        match.start(),
                        match.end(),
                    )
                )

        bare_tier_candidates.sort(
            key=lambda item: (
                item[0],
                item[1],
            )
        )

        for candidate in bare_tier_candidates:

            position = candidate[0]
            canonical_metric = candidate[2]
            alias = candidate[3]
            start = candidate[4]
            end = candidate[5]

            overlaps = False

            for selected_item in selected:

                selected_start = selected_item[3]
                selected_end = selected_item[4]

                if (
                    start < selected_end
                    and end > selected_start
                ):
                    overlaps = True
                    break

            if overlaps:
                continue

            selected.append(
                (
                    position,
                    canonical_metric,
                    alias,
                    start,
                    end,
                )
            )

            break

        # ------------------------------------------------------------
        # Sort by query position.
        # ------------------------------------------------------------

        selected.sort(
            key=lambda item: item[0]
        )

        # ------------------------------------------------------------
        # Remove duplicate canonical metrics.
        # ------------------------------------------------------------

        matches = []

        for (
            _,
            canonical_metric,
            _,
            _,
            _,
        ) in selected:

            if canonical_metric not in matches:
                matches.append(canonical_metric)

        return matches

    # ----------------------------------------------------------------
    # Comparison detection
    # ----------------------------------------------------------------

    def _is_comparison(
        self,
        query: str,
        metrics: List[str],
    ) -> bool:

        if len(metrics) < 2:
            return False

        q = self._normalize(query)

        padded = f" {q} "

        return (
            " compare " in padded
            or " comparison " in padded
            or " versus " in padded
            or " vs " in padded
            or " with " in padded
        )

    # ----------------------------------------------------------------
    # Definition detection
    # ----------------------------------------------------------------

    def _is_definition(self, query: str) -> bool:
        """
        Detect genuine terminology/definition questions.

        Examples:

            Explain CET1
                -> definition

            Explain CET1 capital
                -> definition

            What is CET1?
                -> definition

            Explain why CET1 fell
                -> NOT definition
                -> analysis
        """

        q = self._normalize(query)

        padded = f" {q} "

        # ------------------------------------------------------------
        # Explicit definition language
        # ------------------------------------------------------------

        explicit_definition = (
            " what is " in padded
            or " what are " in padded
            or " what does " in padded
            or " define " in padded
            or " definition " in padded
            or " meaning " in padded
        )

        if explicit_definition:
            return True

        # ------------------------------------------------------------
        # "Explain <metric>"
        #
        # Only treat it as definition when "explain" is not
        # accompanied by causal/analytical language.
        # ------------------------------------------------------------

        if " explain " in padded:

            metrics = self._resolve_metric(q)

            if not metrics:
                return False

            analytical_terms = (
                " why ",
                " reason ",
                " cause ",
                " caused ",
                " driver ",
                " drivers ",
                " impact ",
                " fall ",
                " fell ",
                " drop ",
                " dropped ",
                " decline ",
                " declined ",
                " decrease ",
                " decreased ",
                " increase ",
                " increased ",
                " rise ",
                " rose ",
                " grow ",
                " grew ",
                " growth ",
                " performing ",
                " performance ",
                " analyze ",
                " analysis ",
                " assess ",
                " evaluate ",
            )

            if any(
                term in padded
                for term in analytical_terms
            ):
                return False

            return True

        return False

    # ----------------------------------------------------------------
    # Analysis detection
    # ----------------------------------------------------------------

    def _is_analysis(self, query: str) -> bool:

        q = self._normalize(query)

        padded = f" {q} "

        return (
            # Causal language
            " why " in padded
            or " reason " in padded
            or " cause " in padded
            or " caused " in padded
            or " driver " in padded
            or " drivers " in padded
            or " impact " in padded

            # Directional language
            or " fall " in padded
            or " fell " in padded
            or " falling " in padded
            or " drop " in padded
            or " dropped " in padded
            or " decline " in padded
            or " declined " in padded
            or " declining " in padded
            or " decrease " in padded
            or " decreased " in padded
            or " increasing " in padded
            or " increase " in padded
            or " increased " in padded
            or " rise " in padded
            or " rose " in padded
            or " growing " in padded
            or " grew " in padded
            or " growth " in padded

            # Performance
            or " performing " in padded
            or " performance " in padded

            # Analytical verbs
            or " analyze " in padded
            or " analysis " in padded
            or " assess " in padded
            or " evaluate " in padded
            or " explain " in padded
        )

    # ----------------------------------------------------------------
    # Trend detection
    # ----------------------------------------------------------------

    def _is_trend(self, query: str) -> bool:

        q = self._normalize(query)

        padded = f" {q} "

        return (
            " trend " in padded
            or " over time " in padded
            or " historical " in padded
            or " history " in padded
            or " historically " in padded
        )

    # ----------------------------------------------------------------
    # Main planning function
    # ----------------------------------------------------------------

    def plan(self, query: str) -> ExecutionPlan:

        q = self._normalize(query)

        metrics = self._resolve_metric(q)

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

        if self._is_comparison(q, metrics):

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
        # 2. DEFINITION
        #
        # IMPORTANT:
        # Definition MUST come before general analysis.
        #
        # Therefore:
        #
        # Explain CET1
        # -> definition
        #
        # while:
        #
        # Explain why CET1 fell
        # -> analysis
        # ============================================================

        if self._is_definition(q):

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
        # 3. ANALYSIS
        # ============================================================

        if self._is_analysis(q):

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
        # 4. TREND
        # ============================================================

        if self._is_trend(q):

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
        # 6. GENERAL ANALYSIS
        # ============================================================

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

        # Definitions
        "Explain CET1",
        "Explain CET1 capital",
        "Explain CET1 ratio",
        "Explain Tier 1",
        "Explain Tier 1 capital",
        "Explain Tier 1 ratio",
        "Explain NII",
        "What is CET1?",
        "What does CET1 mean?",
        "Define NII",

        # Analysis
        "Explain why CET1 fell",
        "Explain why CET1 ratio fell",
        "Explain why NII increased",
        "Explain why revenue declined",
        "Why did CET1 fall?",
        "Why did NII increase?",
        "How is CET1 performing?",
        "How is HSBC performing?",
        "Explain the financial performance",

        # Trends
        "Show CET1 trend",
        "Show CET1 ratio trend",
        "Show revenue trend",
        "Show historical revenue",
        "Show CET1 over time",

        # Comparisons
        "Compare CET1 with Tier 1",
        "Compare Tier 1 with CET1",
        "Compare CET1 capital with CET1 ratio",
        "Compare CET1 ratio with CET1 capital",
        "Compare Tier 1 capital with CET1 capital",
        "Compare CET1 capital with Tier 1 capital",
        "Compare Tier 1 ratio with CET1 ratio",
        "Compare CET1 ratio with Tier 1 ratio",
        "Compare NII with Revenue",
        "Compare Revenue with NII",

        # Metric lookup
        "Show CET1",
        "Show CET1 capital",
        "Show CET1 ratio",
        "Show NII",
        "Show revenue",
        "Show PBT",
        "Show ECL",

        # General
        "What happened?",
        "What changed?",
        "Give me an overview",
        "What happened to HSBC?",
    ]

    for query in tests:

        plan = planner.plan(query)

        print("=" * 80)
        print(f"QUERY:       {query}")
        print(f"INTENT:      {plan.intent}")
        print(f"METRIC:      {plan.metric}")
        print(f"COMPARISON:  {plan.comparison_metric}")
        print(
            f"STEPS:       {[step.agent for step in plan.steps]}"
        )
        print(f"NEEDS LLM:   {plan.needs_llm}")