# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from warehouse.query_service import (
    get_metric_by_name,
    get_metric_by_id,
    get_all_metrics,
    search_metrics,
)


class SQLAgent:

    def execute(self, plan):

        if plan.metric is None:
            return None

        if plan.intent == "metric_lookup":
            return get_metric_by_name(plan.metric)

        if plan.intent == "trend":
            return get_metric_by_name(plan.metric)

        if plan.intent == "analysis":
            return get_metric_by_name(plan.metric)

        if plan.intent == "comparison":
            return get_metric_by_name(plan.metric)

        return None

if __name__ == "__main__":

    from planner import Planner

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

        print(plan)

        result = sql.execute(plan)

        if result:
            print(result[:5])
        else:
            print(result)