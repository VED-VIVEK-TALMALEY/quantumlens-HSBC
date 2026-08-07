# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from .execution_context import ExecutionContext
import statistics
# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley
# -------------------------------------------------------------------
class FinancialReasoningAgent:

    def execute(self, context):

        rows = context.sql_result

        if not rows:
            context.financial_reasoning = None
            return context

        periods = []
        values = []

        for row in rows:
            periods.append(str(row[7]))
            values.append(float(row[8]))

        first_value = values[0]
        last_value = values[-1]

        absolute_change = round(last_value - first_value, 2)

        if first_value != 0:
            percent_change = round(
                absolute_change / first_value * 100,
                2
            )
        else:
            percent_change = 0

        if absolute_change > 0:
            direction = "increase"
        elif absolute_change < 0:
            direction = "decrease"
        else:
            direction = "no change"

        highest_value = max(values)
        highest_index = values.index(highest_value)
        highest_period = periods[highest_index]

        lowest_value = min(values)
        lowest_index = values.index(lowest_value)
        lowest_period = periods[lowest_index]

        average = round(sum(values) / len(values), 2)
        median = statistics.median(values)
        volatility = round(statistics.pstdev(values), 2)

        if len(values) > 1:

            latest_change = round(
                values[-1] - values[-2],
                2
            )

            if values[-2] != 0:
                latest_percent_change = round(
                    latest_change / values[-2] * 100,
                    2
                )
            else:
                latest_percent_change = 0

            changes = []

            for i in range(1, len(values)):
                changes.append(values[i] - values[i - 1])

            max_increase = round(max(changes), 2)
            max_decrease = round(min(changes), 2)

        else:

            latest_change = 0
            latest_percent_change = 0
            max_increase = 0
            max_decrease = 0

        if values == sorted(values):

            trend = "consistently increasing"

        elif values == sorted(values, reverse=True):

            trend = "consistently decreasing"

        else:

            trend = "volatile"

        context.financial_reasoning = {

            "first_value": first_value,

            "last_value": last_value,

            "absolute_change": absolute_change,

            "percent_change": percent_change,

            "direction": direction,

            "highest_value": highest_value,
            "highest_period": highest_period,

            "lowest_value": lowest_value,
            "lowest_period": lowest_period,

            "average": average,
            "median": median,

            "volatility": volatility,

            "latest_change": latest_change,
            "latest_percent_change": latest_percent_change,

            "max_increase": max_increase,
            "max_decrease": max_decrease,

            "trend": trend

        }

        return context

# -------------------------------------------------------------------
# Testing
# -------------------------------------------------------------------
if __name__ == "__main__":

    from .planner import Planner
    from .execution_context import ExecutionContext

    planner = Planner()

    plan = planner.plan("Show CET1 trend")

    context = ExecutionContext(
        question="Show CET1 trend",
        plan=plan
    )

    context.sql_result = [
        (0,0,0,"cet1",0,0,0,"1",123996),
        (0,0,0,"cet1",0,0,0,"2",132593),
        (0,0,0,"cet1",0,0,0,"3",127765),
        (0,0,0,"cet1",0,0,0,"4",129819),
        (0,0,0,"cet1",0,0,0,"5",125477),
    ]

    agent = FinancialReasoningAgent()

    context = agent.execute(context)

    print(context.financial_reasoning)