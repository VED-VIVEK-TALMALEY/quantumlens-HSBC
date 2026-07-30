# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from .planner import Planner
from .sql_agent import SQLAgent
from .rag_agent import RAGAgent
from .chart_agent import ChartAgent


class Orchestrator:

    def __init__(self):

        self.planner = Planner()

        self.sql = SQLAgent()

        self.rag = RAGAgent()

        self.chart = ChartAgent()

    def execute(self, question):
        plan = self.planner.plan(question)
        sql_result = None
        rag_result = None
        chart_result = None
        if "sql" in plan.agents:
         sql_result = self.sql.execute(plan)
        if "rag" in plan.agents:
           rag_result = self.rag.execute(question)
        if "chart" in plan.agents and sql_result:

            chart_result = self.chart.execute(
                plan.metric,
                sql_result
    )

        return {

    "plan": plan,

    "sql": sql_result,

    "rag": rag_result,

    "chart": chart_result
}

if __name__ == "__main__":

    orchestrator = Orchestrator()

    tests = [

        "Show CET1",

        "Show CET1 trend",

        "Explain CET1 ratio",

        "Why did CET1 fall?"
    ]

    for q in tests:

        print("=" * 70)

        print(q)

        result = orchestrator.execute(q)

        print(result)