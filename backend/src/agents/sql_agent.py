# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from opentelemetry import context

from warehouse.query_service import (
    get_metric_by_name,
    get_metric_by_id,
    get_all_metrics,
    search_metrics,
)


class SQLAgent:

    def execute(self, context):

        plan = context.plan

        if plan.metric is None:
            context.sql_result = None
            return context

        result = get_metric_by_name(plan.metric)

        print(f"DEBUG - SQLAgent searching for: {plan.metric}")
        print(f"DEBUG - SQLAgent found: {result}")
        context.sql_result = result

        return context


if __name__ == "__main__":

    from src.agents.planner import Planner
    from src.agents.execution_context import ExecutionContext

    planner = Planner()

    sql = SQLAgent()

    tests = [

        "Show CET1",

        "Show CET1 trend",

        "Why did CET1 fall?",

        "Show NII"

    ]

    for q in tests:

        print("=" * 60)

        print(q)

        plan = planner.plan(q)

        context = ExecutionContext(

            question=q,

            plan=plan

        )

        context = sql.execute(context)

        print(context.sql_result)