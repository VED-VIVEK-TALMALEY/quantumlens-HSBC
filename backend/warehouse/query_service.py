"""Supabase-backed metric query helpers."""
from __future__ import annotations
from typing import Any
from warehouse.supabase_client import get_supabase

# Canonical metric names and known abbreviations. Resolution works in either direction.
_ALIAS_GROUPS = (
    ("common_equity_tier_1_capital", "cet1"),
    ("common_equity_tier_1_ratio", "cet1_ratio", "cet1r"),
    ("tier_1_ratio", "tier1", "t1r"),
    ("net_interest_income", "nii"),
    ("net_fee_income", "nfi"),
    ("revenue", "rev"),
    ("profit_before_tax", "pbt"),
    ("total_assets", "assets", "ta"),
    ("total_liabilities", "liabilities", "tl"),
    ("customer_accounts", "ca"),
    ("loans_and_advances_to_customers_net", "loans", "advances", "lacn"),
    ("return_on_average_tangible_equity", "rote"),
    ("expected_credit_losses", "ecl", "expected_credit_loss"),
    ("net_interest_margin", "nim"),
    ("total_operating_expenses", "toe"),
    ("operating_expenses", "opex"),
)
_ALIAS_LOOKUP = {alias: list(group) for group in _ALIAS_GROUPS for alias in group}


def resolve_metric_name(metric: str) -> list[str]:
    key = str(metric or "").strip().lower()
    return _ALIAS_LOOKUP.get(key, [key] if key else [])


def _source_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (row.get("metric_id"), row.get("source_workbook"), row.get("sheet_name"), row.get("row_number"))


def _row_number(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def get_all_metrics():
    client = get_supabase()
    response = client.table("metrics").select("metric_id,metric_name,abbreviation").execute()
    unique = {}
    for row in response.data or []:
        key = (row.get("metric_id"), row.get("metric_name"), row.get("abbreviation"))
        unique[key] = row
    rows = sorted(unique.values(), key=lambda r: (r.get("metric_id") is None, r.get("metric_id") or 0, r.get("metric_name") or ""))
    return [(r.get("metric_id"), r.get("metric_name"), r.get("abbreviation")) for r in rows]


def get_metric_by_id(metric_id: int):
    response = get_supabase().table("metrics").select("*").eq("metric_id", metric_id).execute()
    rows = response.data or []
    return sorted(rows, key=lambda r: ((r.get("sheet_name") or "").lower(), _row_number(r.get("row_number"))))


def get_metric_by_name(metric: str):
    candidates = resolve_metric_name(metric)
    if not candidates:
        return []
    client = get_supabase()
    rows: dict[tuple[Any, ...], dict[str, Any]] = {}
    for candidate in candidates:
        for column in ("metric_name", "abbreviation"):
            response = client.table("metrics").select("*").eq(column, candidate).execute()
            for row in response.data or []:
                rows[_source_key(row)] = row
    result = list(rows.values())
    # Keep group-level records first for charts/reasoning, then stable sheet/row order.
    def sort_key(row):
        sheet = (row.get("sheet_name") or "").lower()
        if sheet == "group income statement": priority = 0
        elif sheet == "group balance sheet": priority = 1
        elif "group" in sheet: priority = 2
        else: priority = 3
        return (priority, sheet, _row_number(row.get("row_number")))
    result.sort(key=sort_key)
    return result


def search_metrics(keyword: str):
    term = str(keyword or "").strip()
    if not term:
        return []
    client = get_supabase()
    rows = []
    for column in ("metric_name", "abbreviation"):
        response = client.table("metrics").select("metric_id,metric_name,abbreviation").ilike(column, f"%{term}%").execute()
        rows.extend(response.data or [])
    unique = {(r.get("metric_id"), r.get("metric_name"), r.get("abbreviation")): r for r in rows}
    result = sorted(unique.values(), key=lambda r: (r.get("metric_name") or "", r.get("metric_id") or 0))
    return [(r.get("metric_id"), r.get("metric_name"), r.get("abbreviation")) for r in result]
