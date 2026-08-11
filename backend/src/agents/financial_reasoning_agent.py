## -------------------------------------------------------------------
## Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
## This project and its source code are strictly proprietary.
## Unauthorized copying, distribution, or use is strictly prohibited.
## -------------------------------------------------------------------

from .execution_context import ExecutionContext
import statistics


class FinancialReasoningAgent:

    def execute(self, context: ExecutionContext):

        rows = context.sql_result

        # ------------------------------------------------------------
        # No SQL data
        # ------------------------------------------------------------

        if not rows:

            context.financial_reasoning = None

            return context

        periods = []
        values = []

        # ------------------------------------------------------------
        # Extract period and value.
        #
        # Current Oracle row structure:
        #
        # row[7] = period
        # row[8] = value
        # ------------------------------------------------------------

        for row in rows:

            try:

                period = str(row[7])
                value = float(row[8])

            except (
                IndexError,
                TypeError,
                ValueError
            ):

                continue

            periods.append(period)
            values.append(value)

        # ------------------------------------------------------------
        # No valid numeric values
        # ------------------------------------------------------------

        if not values:

            context.financial_reasoning = None

            return context

        # ------------------------------------------------------------
        # IMPORTANT HSBC PERIOD ORDER
        #
        # Current ingestion stores:
        #
        # Period 1 = latest
        # Period 2 = previous
        # Period 3 = older
        # ...
        #
        # Therefore:
        #
        # latest_value   = values[0]
        # previous_value = values[1]
        #
        # Do NOT use values[-1] as latest.
        # ------------------------------------------------------------

        latest_value = values[0]
        latest_period = periods[0]

        if len(values) >= 2:

            previous_value = values[1]
            previous_period = periods[1]

        else:

            previous_value = None
            previous_period = None

        # ------------------------------------------------------------
        # Latest-period change
        # ------------------------------------------------------------

        if previous_value is not None:

            latest_change = (
                latest_value
                - previous_value
            )

            if previous_value != 0:

                latest_percent_change = (
                    latest_change
                    / previous_value
                    * 100
                )

            else:

                latest_percent_change = 0.0

        else:

            latest_change = 0.0
            latest_percent_change = 0.0

        # ------------------------------------------------------------
        # Direction
        # ------------------------------------------------------------

        if latest_change > 0:

            direction = "increase"

        elif latest_change < 0:

            direction = "decrease"

        else:

            direction = "no change"

        # ------------------------------------------------------------
        # Historical high / low
        # ------------------------------------------------------------

        highest_value = max(values)

        highest_index = values.index(
            highest_value
        )

        highest_period = periods[
            highest_index
        ]

        lowest_value = min(values)

        lowest_index = values.index(
            lowest_value
        )

        lowest_period = periods[
            lowest_index
        ]

        # ------------------------------------------------------------
        # Historical statistics
        # ------------------------------------------------------------

        average = (
            sum(values)
            / len(values)
        )

        median = statistics.median(
            values
        )

        volatility = statistics.pstdev(
            values
        )

        # ------------------------------------------------------------
        # Historical sequential changes
        #
        # These follow the source order.
        # ------------------------------------------------------------

        

        chronological_values = list(reversed(values))

        changes = []
        for index in range(1, len(chronological_values)):
            changes.append(
        chronological_values[index]
        - chronological_values[index - 1]
    )

        if changes:

            max_increase = max(
                changes
            )

            max_decrease = min(
                changes
            )

        else:

            max_increase = 0.0
            max_decrease = 0.0

        # ------------------------------------------------------------
        # Trend classification
        #
        # Because the newest value is at index 0, the chronological
        # direction is evaluated from the current value backwards.
        # ------------------------------------------------------------

        chronological_values = list(reversed(values))
        if len(chronological_values) < 2:

                trend = "insufficient data"

        elif all(
            chronological_values[index]
            >= chronological_values[index - 1]
                for index in range(1, len(chronological_values))):

                    trend = "consistently increasing"

        elif all(
            chronological_values[index]
                <= chronological_values[index - 1]
                for index in range(1, len(chronological_values))):
             trend = "consistently decreasing"

        else:

            trend = "volatile"
        # ------------------------------------------------------------
        # Store financial reasoning
        # ------------------------------------------------------------

        context.financial_reasoning = {

            # Latest reporting period
            "latest_value":
                round(
                    latest_value,
                    6
                ),

            "latest_period":
                latest_period,

            # Previous reporting period
            "previous_value":
                (
                    round(
                        previous_value,
                        6
                    )
                    if previous_value is not None
                    else None
                ),

            "previous_period":
                previous_period,

            # Latest movement
            "absolute_change":
                round(
                    latest_change,
                    6
                ),

            "percent_change":
                round(
                    latest_percent_change,
                    4
                ),

            "direction":
                direction,

            # Historical extrema
            "highest_value":
                round(
                    highest_value,
                    6
                ),

            "highest_period":
                highest_period,

            "lowest_value":
                round(
                    lowest_value,
                    6
                ),

            "lowest_period":
                lowest_period,

            # Statistics
            "average":
                round(
                    average,
                    6
                ),

            "median":
                round(
                    median,
                    6
                ),

            "volatility":
                round(
                    volatility,
                    6
                ),

            # Latest movement repeated explicitly
            "latest_change":
                round(
                    latest_change,
                    6
                ),

            "latest_percent_change":
                round(
                    latest_percent_change,
                    4
                ),

            # Historical movement range
            "max_increase":
                round(
                    max_increase,
                    6
                ),

            "max_decrease":
                round(
                    max_decrease,
                    6
                ),

            "trend":
                trend
        }

        return context


# -------------------------------------------------------------------
# Testing
# -------------------------------------------------------------------

if __name__ == "__main__":

    from .planner import Planner
    from .execution_context import ExecutionContext

    planner = Planner()

    question = "Why did CET1 fall?"

    plan = planner.plan(
        question
    )

    context = ExecutionContext(
        question=question,
        plan=plan
    )

    # ------------------------------------------------------------
    # HSBC 1Q26 CET1 test data
    #
    # Period 1 = 1Q26 = 14.0%
    # Period 2 = 4Q25 = 14.9%
    # Period 3 = 1Q25 = 14.5%
    # Period 4 = 4Q24 = 14.6%
    # Period 5 = 1Q24 = 14.7%
    # ------------------------------------------------------------

    context.sql_result = [

        (
            0,
            0,
            0,
            "cet1_ratio",
            0,
            0,
            0,
            "1",
            0.140
        ),

        (
            0,
            0,
            0,
            "cet1_ratio",
            0,
            0,
            0,
            "2",
            0.149
        ),

        (
            0,
            0,
            0,
            "cet1_ratio",
            0,
            0,
            0,
            "3",
            0.145
        ),

        (
            0,
            0,
            0,
            "cet1_ratio",
            0,
            0,
            0,
            "4",
            0.146
        ),

        (
            0,
            0,
            0,
            "cet1_ratio",
            0,
            0,
            0,
            "5",
            0.147
        )
    ]

    agent = FinancialReasoningAgent()

    context = agent.execute(
        context
    )

    print(
        context.financial_reasoning
    )