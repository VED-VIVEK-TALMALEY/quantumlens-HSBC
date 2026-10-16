"""SQL-style metric retrieval backed by Supabase."""
from warehouse.query_service import get_metric_by_name


class SQLRetriever:
    def get_metric(self, metric_name: str):
        # Return source records with period_values JSON, not legacy Oracle tuples.
        return get_metric_by_name(metric_name)
