"""Financial reasoning over the JSONB period_values returned by Supabase."""
from __future__ import annotations
import statistics
from .execution_context import ExecutionContext
from .metric_row_utils import select_primary_record, ordered_periods, as_number


class FinancialReasoningAgent:
    def execute(self, context: ExecutionContext):
        record = select_primary_record(context.sql_result)
        periods = ordered_periods(record)
        points = [(p, as_number(p.get("value"))) for p in periods]
        points = [(p, v) for p, v in points if v is not None]
        if not record or not points:
            context.financial_reasoning = None
            return context

        # HSBC source convention: Period 1 is latest; Period 2 is previous.
        latest_period, latest_value = points[0]
        previous_period, previous_value = points[1] if len(points) > 1 else (None, None)
        change = latest_value - previous_value if previous_value is not None else None
        pct_change = (change / previous_value * 100) if previous_value not in (None, 0) else None
        values = [value for _, value in points]
        chronological = list(reversed(values))
        if len(chronological) < 2:
            trend = "insufficient data"
        elif all(chronological[i] >= chronological[i - 1] for i in range(1, len(chronological))):
            trend = "consistently increasing"
        elif all(chronological[i] <= chronological[i - 1] for i in range(1, len(chronological))):
            trend = "consistently decreasing"
        else:
            trend = "volatile"

        context.financial_reasoning = {
            "metric_id": record.get("metric_id"),
            "metric_name": record.get("metric_name"),
            "abbreviation": record.get("abbreviation"),
            "source_workbook": record.get("source_workbook"),
            "sheet_name": record.get("sheet_name"),
            "row_number": record.get("row_number"),
            "latest_value": latest_value,
            "latest_period": latest_period.get("period_label") or f"Period {latest_period.get('period_index', 1)}",
            "previous_value": previous_value,
            "previous_period": (previous_period.get("period_label") or f"Period {previous_period.get('period_index', 2)}") if previous_period else None,
            "absolute_change": change,
            "percent_change": pct_change,
            "direction": "increase" if change is not None and change > 0 else "decrease" if change is not None and change < 0 else "no change" if change is not None else "insufficient data",
            "highest_value": max(values),
            "highest_period": next((p.get("period_label") for p, v in points if v == max(values)), None),
            "lowest_value": min(values),
            "lowest_period": next((p.get("period_label") for p, v in points if v == min(values)), None),
            "average": statistics.mean(values),
            "median": statistics.median(values),
            "volatility": statistics.pstdev(values) if len(values) > 1 else 0.0,
            "trend": trend,
            "period_order": "Period 1 is latest; Period 2 is previous",
            "data_points": len(values),
        }
        return context
