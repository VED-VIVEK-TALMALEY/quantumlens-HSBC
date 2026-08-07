# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# -------------------------------------------------------------------

from dataclasses import dataclass


@dataclass
class ExecutionContext:

    question: str

    plan: object

    sql_result: object = None

    rag_result: object = None

    chart_result: object = None

    llm_result: object = None

    audit_result: object = None
    reasoning_result = None
    financial_reasoning = None