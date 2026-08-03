# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from .execution_context import ExecutionContext

class ResponseAgent:
    def execute(self, context: ExecutionContext):
        # --- Step 2: Extract variables from context ---
        plan = context.plan
        sql_result = context.sql_result
        chart_result = context.chart_result
        rag_result = context.rag_result
        audit_result = context.audit_result
        llm_result = context.llm_result

        confidence = (
            audit_result["confidence"]
            if audit_result else 1.0
        )

        warnings = (
            audit_result["warnings"]
            if audit_result else []
        )

        # -------------------------------------------------------
        # LLM Response (Only when planner explicitly requests it)
        # -------------------------------------------------------

        if plan.needs_llm and llm_result is not None:
            return {
                "status": "success",
                "intent": plan.intent,
                "metric": plan.metric,
                "answer": llm_result["answer"],
                "chart": chart_result,
                "confidence": confidence,
                "warnings": warnings,
                "provider": llm_result["provider"],
                "model": llm_result["model"]
            }

        # -------------------------------------------------------
        # Metric Lookup
        # -------------------------------------------------------

        if plan.intent == "metric_lookup":
            if not sql_result:
                return {
                    "status": "error",
                    "answer": "No data found.",
                    "confidence": confidence,
                    "warnings": warnings
                }

            latest = sql_result[-1]

            return {
                "status": "success",
                "intent": plan.intent,
                "metric": plan.metric,
                "answer": f"Latest {plan.metric.upper()} = {latest[8]:,}",
                "data": latest,
                "confidence": confidence,
                "warnings": warnings
            }

        # -------------------------------------------------------
        # Trend
        # -------------------------------------------------------

        elif plan.intent == "trend":
            if not sql_result:
                return {
                    "status": "error",
                    "answer": "No trend data found.",
                    "confidence": confidence,
                    "warnings": warnings
                }

            first = sql_result[0][8]
            last = sql_result[-1][8]

            change = last - first

            if change > 0:
                direction = "increased"
            elif change < 0:
                direction = "decreased"
            else:
                direction = "remained unchanged"

            return {
                "status": "success",
                "intent": plan.intent,
                "metric": plan.metric,
                "answer": f"{plan.metric.upper()} {direction} from {first:,} to {last:,}.",
                "chart": chart_result,
                "confidence": confidence,
                "warnings": warnings
            }

        # -------------------------------------------------------
        # Definition
        # -------------------------------------------------------

        elif plan.intent == "definition":
            return {
                "status": "success",
                "intent": plan.intent,
                "metric": plan.metric,
                "answer": rag_result,
                "confidence": confidence,
                "warnings": warnings
            }

        # -------------------------------------------------------
        # Analysis
        # -------------------------------------------------------

        elif plan.intent == "analysis":

            return {

        "status": "error",

        "answer": "Analysis requested but no LLM response was generated.",

        "confidence": confidence,

        "warnings": warnings

    }

        # -------------------------------------------------------
        # Comparison
        # -------------------------------------------------------

        elif plan.intent == "comparison":
            return {
                "status": "success",
                "intent": plan.intent,
                "metric": plan.metric,
                "chart": chart_result,
                "data": sql_result,
                "confidence": confidence,
                "warnings": warnings
            }

        # -------------------------------------------------------
        # Unknown
        # -------------------------------------------------------

        return {
            "status": "error",
            "answer": "Unsupported query.",
            "confidence": 0.0,
            "warnings": ["Planner returned an unknown intent."]
        }


# -------------------------------------------------------------------
# Testing
# -------------------------------------------------------------------

if __name__ == "__main__":
    from .planner import Planner

    planner = Planner()
    response = ResponseAgent()
    plan = planner.plan("Show CET1 trend")

    fake_sql = [
        (1, 2, 3, "cet1", 5, 6, 7, "1", 123996),
        (1, 2, 3, "cet1", 5, 6, 7, "2", 132593),
        (1, 2, 3, "cet1", 5, 6, 7, "3", 127765),
        (1, 2, 3, "cet1", 5, 6, 7, "4", 129819),
        (1, 2, 3, "cet1", 5, 6, 7, "5", 125477)
    ]

    fake_chart = {
        "chart_type": "line",
        "title": "CET1",
        "x": ["1", "2", "3", "4", "5"],
        "y": [123996, 132593, 127765, 129819, 125477]
    }

    fake_audit = {
        "confidence": 1.0,
        "warnings": []
    }

    # --- Step 3: Wrap inputs in ExecutionContext ---
    context = ExecutionContext(
        question="Show CET1 trend",
        plan=plan,
        sql_result=fake_sql,
        chart_result=fake_chart,
        rag_result=None,
        audit_result=fake_audit,
        llm_result=None
    )

    result = response.execute(context)
    print(result)