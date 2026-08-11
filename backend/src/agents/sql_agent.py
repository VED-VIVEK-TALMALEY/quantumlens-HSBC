## -------------------------------------------------------------------
## Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
##
## This project and its source code are strictly proprietary.
## Unauthorized copying, distribution, or use is strictly prohibited.
## -------------------------------------------------------------------


from warehouse.query_service import get_metric_by_name

from .execution_context import ExecutionContext


class SQLAgent:
    def execute(self, context):
        plan = context.plan

    # Primary metric
        if plan.metric is not None:

            context.sql_result = get_metric_by_name(
            plan.metric
        )

        else:

            context.sql_result = None

    # Comparison metric
        if plan.comparison_metric is not None:

            context.comparison_sql_result = (
            get_metric_by_name(
                plan.comparison_metric
            )
        )

        else:

            context.comparison_sql_result = None

        print(
        f"DEBUG - SQLAgent primary metric: "
        f"{plan.metric}"
    )

        print(
        f"DEBUG - SQLAgent comparison metric: "
        f"{plan.comparison_metric}"
    )

        print(
        f"DEBUG - SQL primary rows: "
        f"{len(context.sql_result or [])}"
    )

        print(
        f"DEBUG - SQL comparison rows: "
        f"{len(context.comparison_sql_result or [])}"
    )

        return context


## -------------------------------------------------------------------
## Testing
## -------------------------------------------------------------------

if __name__ == "__main__":
    from src.agents.planner import Planner

    planner = Planner()
    sql = SQLAgent()

    tests = [
        "Show CET1",
        "Show CET1 capital",
        "Show CET1 ratio",
        "Show CET1 capital ratio",
        "Why did CET1 ratio fall?",
        "Show CET1 ratio trend",
        "Show NII",
        "Show NII trend",
        "Show PBT trend",
    ]

    for q in tests:
        print("=" * 70)
        print(q)

        plan = planner.plan(q)

        print(
            f"DEBUG - Plan metric: "
            f"{plan.metric}"
        )

        context = ExecutionContext(
            question=q,
            plan=plan
        )

        context = sql.execute(
            context
        )

        print(
            "SQL RESULT:"
        )

        print(
            context.sql_result
        )