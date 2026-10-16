"""Helpers for the Supabase JSONB metric-record shape."""
from __future__ import annotations
from typing import Any


def as_number(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def select_primary_record(rows: list[dict[str, Any]] | None) -> dict[str, Any] | None:
    if not rows:
        return None
    def key(row):
        sheet = (row.get("sheet_name") or "").strip().lower()
        if sheet == "group income statement": priority = 0
        elif sheet == "group balance sheet": priority = 1
        elif "group" in sheet: priority = 2
        else: priority = 3
        try: row_number = int(row.get("row_number") or 0)
        except (TypeError, ValueError): row_number = 0
        return (priority, sheet, row_number)
    return sorted(rows, key=key)[0]


def ordered_periods(record: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not record:
        return []
    values = record.get("period_values") or []
    valid = [dict(p) for p in values if isinstance(p, dict) and p.get("value") is not None]
    def key(period):
        try: return int(period.get("period_index", 10**9))
        except (TypeError, ValueError): return 10**9
    return sorted(valid, key=key)
