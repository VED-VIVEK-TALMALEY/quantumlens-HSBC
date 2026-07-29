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
         result = get_metric_by_name(plan.metric)
         print(f"DEBUG - SQLAgent searching for: {plan.metric}")
         print(f"DEBUG - SQLAgent found: {result}")

         if plan.intent == "metric_lookup":
             return result

         if plan.intent == "trend":
             return result

         if plan.intent == "analysis":
            return result

         if plan.intent == "comparison":
            return result

         return None

if __name__ == "__main__":

        from src.agents.planner import Planner

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
