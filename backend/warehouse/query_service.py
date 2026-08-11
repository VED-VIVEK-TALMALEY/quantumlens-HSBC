# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
#
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from warehouse.supabase_client import get_supabase

# -------------------------------------------------------------------
# Canonical Metric Mapping
# -------------------------------------------------------------------

METRIC_ALIASES = {
    "cet1": [
        "common_equity_tier_1_capital",
        "cet1",
    ],
    "cet1_ratio": [
        "common_equity_tier_1_ratio",
        "cet1r",
    ],
    "tier1": [
        "tier_1_ratio",
        "t1r",
    ],
    "nii": [
        "net_interest_income",
        "nii",
    ],
    "nfi": [
        "net_fee_income",
        "nfi",
    ],
    "revenue": [
        "revenue",
        "rev",
    ],
    "profit_before_tax": [
        "profit_before_tax",
        "pbt",
    ],
    "assets": [
        "assets",
        "total_assets",
    ],
    "liabilities": [
        "liabilities",
        "total_liabilities",
    ],
    "customer_accounts": [
        "customer_accounts",
        "ca",
    ],
    "loans": [
        "loans",
        "gross_loans",
        "advances",
    ],
    "rote": [
        "rote",
        "return_on_average_tangible_equity",
    ],
    "ecl": [
        "ecl",
        "expected_credit_loss",
        "expected_credit_losses",
    ],
}

# -------------------------------------------------------------------
# Resolve canonical metric name
# -------------------------------------------------------------------

def resolve_metric_name(metric):
    """
    Resolve a user-provided metric name or abbreviation
    into the canonical metric candidates used in Supabase.
    """
    metric = metric.lower().strip()

    aliases = METRIC_ALIASES.get(metric)

    if aliases:
        return aliases

    return [metric]

# -------------------------------------------------------------------
# Get all metrics
# -------------------------------------------------------------------

def get_all_metrics():
    """
    Return distinct metrics available in the Supabase
    metrics table.
    """
    supabase = get_supabase()

    response = (
        supabase
        .table("metrics")
        .select("metric_id,metric_name,abbreviation")
        .execute()
    )

    rows = response.data or []

    # Supabase does not provide the same GROUP BY behaviour
    # as the previous Oracle query, so deduplicate in Python.
    unique_metrics = {}

    for row in rows:

        key = (
            row.get("metric_id"),
            row.get("metric_name"),
            row.get("abbreviation"),
        )

        unique_metrics[key] = row

    result = list(unique_metrics.values())

    result.sort(
        key=lambda row: (
            row.get("metric_id")
            if row.get("metric_id") is not None
            else float("inf")
        )
    )

    return [
        (
            row.get("metric_id"),
            row.get("metric_name"),
            row.get("abbreviation"),
        )
        for row in result
    ]

# -------------------------------------------------------------------
# Get metric by ID
# -------------------------------------------------------------------

def get_metric_by_id(metric_id):
    """
    Return all source records belonging to a metric ID.
    """
    supabase = get_supabase()

    response = (
        supabase
        .table("metrics")
        .select("*")
        .eq("metric_id", metric_id)
        .execute()
    )

    rows = response.data or []

    return rows

# -------------------------------------------------------------------
# Get metric by canonical name / abbreviation
#
# IMPORTANT:
#
# Period 1 is the latest period in the current HSBC
# ingestion model.
#
# period_values is stored as JSON/JSONB inside each
# metric record.
#
# Therefore the query service retrieves the source
# records first. Period ordering is handled from
# period_values below.
#
# -------------------------------------------------------------------

def get_metric_by_name(metric):
    """
    Retrieve metric records from Supabase using the
    canonical metric aliases.
    """
    metric = metric.lower().strip()

    candidates = resolve_metric_name(metric)

    supabase = get_supabase()

    rows = []

    # ---------------------------------------------------------------
    # Supabase/PostgREST does not use Oracle-style named bind
    # parameters. Query each candidate independently.
    # ---------------------------------------------------------------

    for candidate in candidates:

        # Search metric_name
        name_response = (
            supabase
            .table("metrics")
            .select("*")
            .eq("metric_name", candidate)
            .execute()
        )

        rows.extend(name_response.data or [])

        # Search abbreviation
        abbreviation_response = (
            supabase
            .table("metrics")
            .select("*")
            .eq("abbreviation", candidate)
            .execute()
        )

        rows.extend(abbreviation_response.data or [])

    # ---------------------------------------------------------------
    # Remove duplicate records.
    # ---------------------------------------------------------------

    unique_rows = {}

    for row in rows:

        # Prefer the source identity when available.
        key = (
            row.get("metric_id"),
            row.get("source_workbook"),
            row.get("sheet_name"),
            row.get("row_number"),
        )

        unique_rows[key] = row

    rows = list(unique_rows.values())

    # ---------------------------------------------------------------
    # Sort by source order.
    # ---------------------------------------------------------------

    rows.sort(
        key=lambda row: (
            row.get("sheet_name") or "",
            row.get("row_number") or 0,
        )
    )

    print(
        f"DEBUG - query_service metric={metric}"
    )

    print(
        f"DEBUG - resolved candidates={candidates}"
    )

    print(
        f"DEBUG - rows found={len(rows)}"
    )

    return rows

# -------------------------------------------------------------------
# Search metrics
# -------------------------------------------------------------------

def search_metrics(keyword):
    """
    Search metric names and abbreviations.
    Uses Supabase text matching instead of Oracle SQL.
    """
    keyword = keyword.lower().strip()

    supabase = get_supabase()

    # ---------------------------------------------------------------
    # Search metric_name
    # ---------------------------------------------------------------

    name_response = (
        supabase
        .table("metrics")
        .select("metric_id,metric_name,abbreviation")
        .ilike("metric_name", f"%{keyword}%")
        .execute()
    )

    # ---------------------------------------------------------------
    # Search abbreviation
    # ---------------------------------------------------------------

    abbreviation_response = (
        supabase
        .table("metrics")
        .select("metric_id,metric_name,abbreviation")
        .ilike("abbreviation", f"%{keyword}%")
        .execute()
    )

    rows = (
        (name_response.data or [])
        + (abbreviation_response.data or [])
    )

    # ---------------------------------------------------------------
    # Deduplicate
    # ---------------------------------------------------------------

    unique_metrics = {}

    for row in rows:

        key = (
            row.get("metric_id"),
            row.get("metric_name"),
            row.get("abbreviation"),
        )

        unique_metrics[key] = row

    result = list(unique_metrics.values())

    result.sort(
        key=lambda row: row.get("metric_name") or ""
    )

    return [
        (
            row.get("metric_id"),
            row.get("metric_name"),
            row.get("abbreviation"),
        )
        for row in result
    ]

# -------------------------------------------------------------------
# Testing
# -------------------------------------------------------------------

if __name__ == "__main__":

    print("=" * 70)
    print("SEARCH EBITDA")
    print("=" * 70)

    print(
        search_metrics("EBITDA")
    )

    print("\n" + "=" * 70)
    print("FIRST 10 METRICS")
    print("=" * 70)

    metrics = get_all_metrics()

    for row in metrics[:10]:
        print(row)

    print("\n" + "=" * 70)
    print("CET1")
    print("=" * 70)

    cet1_rows = get_metric_by_name("cet1")

    print(
        f"Rows returned: {len(cet1_rows)}"
    )

    for row in cet1_rows[:5]:
        print(row)

    print("\n" + "=" * 70)
    print("CET1 RATIO")
    print("=" * 70)

    cet1_ratio_rows = get_metric_by_name(
        "cet1_ratio"
    )

    print(
        f"Rows returned: {len(cet1_ratio_rows)}"
    )

    for row in cet1_ratio_rows[:5]:
        print(row)

    print("\n" + "=" * 70)
    print("TIER 1")
    print("=" * 70)

    tier1_rows = get_metric_by_name("tier1")

    print(
        f"Rows returned: {len(tier1_rows)}"
    )

    for row in tier1_rows[:5]:
        print(row)

    print("\n" + "=" * 70)
    print("PBT")
    print("=" * 70)

    pbt_rows = get_metric_by_name(
        "profit_before_tax"
    )

    print(
        f"Rows returned: {len(pbt_rows)}"
    )

    for row in pbt_rows[:5]:
        print(row)