# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley.
# -------------------------------------------------------------------

from .execution_context import ExecutionContext
from .output_formatter import OutputFormatter


class ResponseAgent:

    def __init__(self):

        self.formatter = OutputFormatter()

    # -------------------------------------------------------------

    def execute(self, context: ExecutionContext):

        plan = context.plan

        # ---------------------------------------------------------
        # LLM Analysis
        # ---------------------------------------------------------

        if plan.needs_llm:

            return self.formatter.format_analysis(context)

        # ---------------------------------------------------------
        # Definition
        # ---------------------------------------------------------

        if plan.intent == "definition":

            return self.formatter.format_definition(context)

        # ---------------------------------------------------------
        # Trend
        # ---------------------------------------------------------

        if plan.intent == "trend":

            return self.formatter.format_trend(context)

        # ---------------------------------------------------------
        # Metric Lookup
        # ---------------------------------------------------------

        if plan.intent == "metric_lookup":

            return self.formatter.format_metric(context)

        # ---------------------------------------------------------
        # Comparison
        # ---------------------------------------------------------

        if plan.intent == "comparison":

            return {

                "status": "success",

                "intent": plan.intent,

                "metric": plan.metric,

                "reasoning": context.financial_reasoning,

                "chart": context.chart_result,

                "confidence": context.audit_result["confidence"]
                if context.audit_result else 1.0,

                "warnings": context.audit_result["warnings"]
                if context.audit_result else []

            }

        # ---------------------------------------------------------

        return {

            "status": "error",

            "answer": "Unsupported query."

        }