"""Build chart-ready data from Supabase metric records."""
from .execution_context import ExecutionContext
from .metric_row_utils import select_primary_record, ordered_periods, as_number


class ChartAgent:
    def execute(self, context: ExecutionContext):
        record = select_primary_record(context.sql_result)
        periods = ordered_periods(record)
        points = [(p.get("period_label") or f"Period {p.get('period_index', '?')}", as_number(p.get("value"))) for p in periods]
        points = [(label, value) for label, value in points if value is not None]
        if not record or not points:
            context.chart_result = None
            return context
        context.chart_result = {
            "chart_type": "line",
            "title": context.plan.metric or record.get("metric_name") or "Metric trend",
            "x": [label for label, _ in points],
            "y": [value for _, value in points],
            "source": {
                "metric_id": record.get("metric_id"),
                "metric_name": record.get("metric_name"),
                "sheet_name": record.get("sheet_name"),
                "row_number": record.get("row_number"),
                "source_workbook": record.get("source_workbook"),
            },
            "period_order": "Period 1 is latest; Period 2 is previous",
        }
        return context
