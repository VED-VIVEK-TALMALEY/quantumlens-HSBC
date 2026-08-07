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

        return {
            "status": "success",
            "intent": context.plan.intent,
            "metric": context.plan.metric,
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

        latest = context.sql_result[-1]

        return {

            "status": "success",

            "intent": context.plan.intent,

            "metric": latest[3],

            "period": latest[7],

            "value": latest[8],

            "confidence": context.audit_result["confidence"]
            if context.audit_result else 1.0,

            "warnings": context.audit_result["warnings"]
            if context.audit_result else [],

        }

    # -----------------------------------------------------

    def format_trend(self, context):

        return {

            "status": "success",

            "intent": context.plan.intent,

            "metric": context.plan.metric,

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