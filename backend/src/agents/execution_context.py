# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# -------------------------------------------------------------------

from dataclasses import dataclass
from dataclasses import dataclass, field


@dataclass
class ExecutionContext:

    question: str
    plan: object

    sql_result: list = field(
        default_factory=list
    )

    comparison_sql_result: list = field(
        default_factory=list
    )

    audit_result: object = None

    financial_reasoning: object = None

    rag_result: object = None

    llm_result: object = None

    chart_result: object = None