# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley.
# -------------------------------------------------------------------


class OutputFormatter:

    def format_definition(self, context):

        metric_docs = context.rag_result.get("metrics", [])
        document_docs = context.rag_result.get("documents", [])

        definition = ""

        if metric_docs:
            definition = metric_docs[0]["text"]

        evidence = ""

        if document_docs:
            evidence = document_docs[0]["text"]
            page = document_docs[0]["metadata"].get("page", "?")
        else:
            page = None

        answer_parts = []
        if definition:
            answer_parts.append(definition)
        if evidence:
            answer_parts.append(f"**Documentary Evidence** (Page {page or 'N/A'}):\n{evidence}")
        answer = "\n\n".join(answer_parts) if answer_parts else f"Definition for {context.plan.metric}."

        return {
            "status": "success",
            "intent": context.plan.intent,
            "metric": context.plan.metric,
            "answer": answer,
            "definition": definition,
            "evidence": evidence,
            "page": page,
            "confidence": context.audit_result["confidence"]
            if context.audit_result else 1.0,
            "warnings": context.audit_result["warnings"]
            if context.audit_result else [],
        }

    # -----------------------------------------------------

    def format_metric(self, context):

        metric_name = context.plan.metric or "metric"
        period = "Latest Period"
        value = None

        if context.sql_result:
            first_row = context.sql_result[0]
            if isinstance(first_row, dict):
                from .metric_row_utils import select_primary_record, ordered_periods
                record = select_primary_record(context.sql_result)
                if record:
                    metric_name = record.get("metric_name") or metric_name
                    periods = ordered_periods(record)
                    if periods:
                        period = periods[0].get("period_label") or f"Period {periods[0].get('period_index', 1)}"
                        value = periods[0].get("value")
            elif isinstance(first_row, (list, tuple)):
                latest = context.sql_result[-1]
                metric_name = latest[3] if len(latest) > 3 else metric_name
                period = latest[7] if len(latest) > 7 else period
                value = latest[8] if len(latest) > 8 else None

        val_str = f"${value:,.2f}M" if isinstance(value, (int, float)) else str(value if value is not None else "N/A")
        answer = f"**{metric_name}**: The reported value for {period} is **{val_str}**."

        return {

            "status": "success",

            "intent": context.plan.intent,

            "metric": metric_name,

            "answer": answer,

            "period": period,

            "value": value,

            "confidence": context.audit_result["confidence"]
            if context.audit_result else 1.0,

            "warnings": context.audit_result["warnings"]
            if context.audit_result else [],

        }

    # -----------------------------------------------------

    def format_trend(self, context):

        reasoning = context.financial_reasoning or ""
        answer = reasoning if reasoning else f"Financial trend analysis for {context.plan.metric}."

        return {

            "status": "success",

            "intent": context.plan.intent,

            "metric": context.plan.metric,

            "answer": answer,

            "reasoning": context.financial_reasoning,

            "chart": context.chart_result,

            "confidence": context.audit_result["confidence"]
            if context.audit_result else 1.0,

            "warnings": context.audit_result["warnings"]
            if context.audit_result else [],

        }

    # -----------------------------------------------------

    def format_analysis(self, context):

        return {

            "status": "success",

            "intent": context.plan.intent,

            "metric": context.plan.metric,

            "answer": context.llm_result["answer"],

            "provider": context.llm_result["provider"],

            "model": context.llm_result["model"],

            "financial_reasoning": context.financial_reasoning,

            "confidence": context.audit_result["confidence"]
            if context.audit_result else 1.0,

            "warnings": context.audit_result["warnings"]
            if context.audit_result else [],

        }