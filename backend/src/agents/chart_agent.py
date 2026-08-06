# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from .execution_context import ExecutionContext


class ChartAgent:

    def execute(self, context: ExecutionContext):

        rows = context.sql_result
        metric_name = context.plan.metric

        if not rows:
            context.chart_result = None
            return context

        x = []
        y = []

        for row in rows:
            x.append(row[7])   # period
            y.append(row[8])   # value

        context.chart_result = {
            "chart_type": "line",
            "title": metric_name,
            "x": x,
            "y": y
        }

        return context


# -------------------------------------------------------------------
# Testing
# -------------------------------------------------------------------

if __name__ == "__main__":

    from .planner import Planner
    from .sql_agent import SQLAgent
    from .execution_context import ExecutionContext

    planner = Planner()
    sql = SQLAgent()
    chart = ChartAgent()

    plan = planner.plan("Show CET1 trend")

    context = ExecutionContext(
        question="Show CET1 trend",
        plan=plan
    )

    context = sql.execute(context)
    context = chart.execute(context)

    print(context.chart_result)