"""Supabase repository adapter; returns dictionaries rather than Oracle tuples."""
from __future__ import annotations
from typing import Any
from warehouse.supabase_client import get_supabase


class MetricRepository:
    def __init__(self, client=None):
        self.client = client or get_supabase()

    def get_all_metrics(self):
        response = self.client.table("metrics").select("metric_id,metric_name,abbreviation").execute()
        unique = {(r.get("metric_id"), r.get("metric_name"), r.get("abbreviation")): r for r in (response.data or [])}
        return sorted(unique.values(), key=lambda r: (r.get("metric_id") or 0, r.get("metric_name") or ""))

    def get_metric(self, metric_id: int):
        response = self.client.table("metrics").select("*").eq("metric_id", metric_id).execute()
        return response.data or []

    def search_metric(self, name: str):
        term = (name or "").strip()
        if not term: return []
        response = self.client.table("metrics").select("metric_id,metric_name,abbreviation").ilike("metric_name", f"%{term}%").execute()
        return response.data or []

    def get_latest_value(self, metric_id: int):
        rows = self.get_metric(metric_id)
        if not rows: return None
        rows.sort(key=lambda r: (0 if (r.get("sheet_name") or "").lower() == "group income statement" else 1, (r.get("sheet_name") or "").lower(), int(r.get("row_number") or 0)))
        periods = rows[0].get("period_values") or []
        periods = sorted(periods, key=lambda p: int(p.get("period_index", 10**9)))
        return periods[0].get("value") if periods else None
