## -------------------------------------------------------------------
## Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
## -------------------------------------------------------------------
import re

class ConversationMemory:
    def __init__(self):
        self.last_metric = None
        self.last_comparison_metric = None
        self.last_intent = None
        self.last_plan = None
        self.last_question = None

    # ----------------------------------------------------------------
    # Reference detection
    # ----------------------------------------------------------------

    @staticmethod
    def _has_reference(question: str) -> bool:
        """
        Detect conversational references.

        Examples:
            Explain it
            Why did it fall?
            Compare it with Tier 1
            What about this?
        """
        q = question.lower()

        return bool(
            re.search(
                r"\b(it|this|that|they|them)\b",
                q,
            )
        )

    # ----------------------------------------------------------------
    # Replace standalone references
    # ----------------------------------------------------------------

    @staticmethod
    def _replace_reference(
        question: str,
        replacement: str,
    ) -> str:
        return re.sub(
            r"\b(it|this|that|they|them)\b",
            replacement,
            question,
            flags=re.IGNORECASE,
        )

    # ----------------------------------------------------------------
    # Resolve conversational question
    # ----------------------------------------------------------------

    def resolve(self, question: str) -> str:
        if not question:
            return question

        question = question.strip()

        # ------------------------------------------------------------
        # No previous context
        # ------------------------------------------------------------

        if self.last_plan is None:
            return question

        # ------------------------------------------------------------
        # No conversational reference
        # ------------------------------------------------------------

        if not self._has_reference(question):
            return question

        metric = self.last_metric
        comparison_metric = self.last_comparison_metric
        intent = self.last_intent
        previous_question = self.last_question

        # ------------------------------------------------------------
        # No metric available
        # ------------------------------------------------------------

        if metric is None:

            if intent in {
                "analysis",
                "general_analysis",
            }:

                return self._replace_reference(
                    question,
                    "the financial performance",
                )

            return question

        # ------------------------------------------------------------
        # DEFINITION
        #
        # What is CET1?
        # Explain it
        #
        # -> Explain cet1_ratio
        # ------------------------------------------------------------

        if intent == "definition":

            return self._replace_reference(
                question,
                metric,
            )

        # ------------------------------------------------------------
        # ANALYSIS
        #
        # Why did CET1 fall?
        # Explain it
        #
        # IMPORTANT:
        # Preserve the previous analytical question.
        # ------------------------------------------------------------

        if intent == "analysis":

            if previous_question:

                return self._replace_reference(
                    question,
                    metric,
                ) + f" Context: {previous_question}"

            return f"Explain {metric}"

        # ------------------------------------------------------------
        # TREND
        #
        # Show CET1 trend
        # Explain it
        #
        # -> Explain cet1_ratio trend
        # ------------------------------------------------------------

        if intent == "trend":

            return self._replace_reference(
                question,
                f"{metric} trend",
            )

        # ------------------------------------------------------------
        # COMPARISON
        #
        # Compare CET1 with Tier 1
        # Explain it
        #
        # Preserve both metrics.
        # ------------------------------------------------------------

        if intent == "comparison":

            if comparison_metric:

                return self._replace_reference(
                    question,
                    f"{metric} with {comparison_metric}",
                )

            return self._replace_reference(
                question,
                metric,
            )

        # ------------------------------------------------------------
        # METRIC LOOKUP
        # ------------------------------------------------------------

        if intent == "metric_lookup":

            return self._replace_reference(
                question,
                metric,
            )

        # ------------------------------------------------------------
        # GENERAL FALLBACK
        # ------------------------------------------------------------

        return self._replace_reference(
            question,
            metric,
        )

    # ----------------------------------------------------------------
    # Store execution plan
    # ----------------------------------------------------------------

    def update(
        self,
        plan,
        question=None,
    ):
        self.last_metric = plan.metric

        self.last_comparison_metric = getattr(
            plan,
            "comparison_metric",
            None,
        )

        self.last_intent = plan.intent

        self.last_plan = plan

        if question is not None:
            self.last_question = question