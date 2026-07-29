# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

class ChartAgent:

    def execute(self, metric_name, rows):

        if not rows:
            return None

        x = []
        y = []

        for row in rows:
           x.append(row[7])      # period
           y.append(row[8])     
            # value     # value

        return {
            "chart_type": "line",
            "title": metric_name,
            "x": x,
            "y": y
        }
  
    

from .planner import Planner
from .sql_agent import SQLAgent
from .chart_agent import ChartAgent


planner = Planner()
sql = SQLAgent()
chart = ChartAgent()

plan = planner.plan("Show CET1 trend")

print(plan)

rows = sql.execute(plan)

print(rows)

chart_data = chart.execute(plan.metric, rows)

print(chart_data)