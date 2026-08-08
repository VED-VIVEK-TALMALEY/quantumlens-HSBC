# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from warehouse.oracle_client import get_connection

# -------------------------------------------------------------------
# Canonical Metric Mapping
# -------------------------------------------------------------------
# Planner canonical names
# ↓
# Actual database metric names / abbreviations
#
# This prevents the Planner vocabulary from being tightly coupled
# to the exact Oracle metric_name values.
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
    ],
    "loans": [
        "loans",
        "gross_loans",
        "advances",
    ],
    "rote": [
        "rote",
        "return_on_tangible_equity",
    ],
    "ecl": [
        "ecl",
        "expected_credit_loss",
        "expected_credit_losses",
    ],
}


# -------------------------------------------------------------------
# Get all metrics
# -------------------------------------------------------------------
def get_all_metrics():
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            SELECT
                metric_id,
                metric_name,
                abbreviation
            FROM metrics
            GROUP BY
                metric_id,
                metric_name,
                abbreviation
            ORDER BY metric_id
            """
        )
        return cur.fetchall()

    finally:
        cur.close()
        conn.close()


# -------------------------------------------------------------------
# Get metric by ID
# -------------------------------------------------------------------
def get_metric_by_id(metric_id):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            SELECT *
            FROM metrics
            WHERE metric_id = :1
            ORDER BY period
            """,
            [metric_id],
        )
        return cur.fetchall()

    finally:
        cur.close()
        conn.close()


# -------------------------------------------------------------------
# Resolve canonical metric name
# -------------------------------------------------------------------
def resolve_metric_name(metric):
    metric = metric.lower().strip()
    aliases = METRIC_ALIASES.get(metric)

    if aliases:
        return aliases

    return [metric]


# -------------------------------------------------------------------
# Get metric by canonical name / abbreviation
# -------------------------------------------------------------------
def get_metric_by_name(metric):
    conn = get_connection()
    cur = conn.cursor()

    try:
        metric = metric.lower().strip()
        candidates = resolve_metric_name(metric)

        conditions = []
        bind_values = {}

        for index, candidate in enumerate(candidates):
            name_key = f"name_{index}"
            abbreviation_key = f"abbr_{index}"

            conditions.append(
                f"""
                LOWER(metric_name) = LOWER(:{name_key})
                OR LOWER(abbreviation) = LOWER(:{abbreviation_key})
                """
            )

            bind_values[name_key] = candidate
            bind_values[abbreviation_key] = candidate

        where_clause = " OR ".join(f"({condition})" for condition in conditions)

        query = f"""
            SELECT *
            FROM metrics
            WHERE {where_clause}
            ORDER BY period
        """

        cur.execute(query, bind_values)
        rows = cur.fetchall()

        print(f"DEBUG - query_service metric={metric}")
        print(f"DEBUG - resolved candidates={candidates}")
        print(f"DEBUG - rows found={len(rows)}")

        return rows

    finally:
        cur.close()
        conn.close()


# -------------------------------------------------------------------
# Search metrics
# -------------------------------------------------------------------
def search_metrics(keyword):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            SELECT DISTINCT
                metric_id,
                metric_name,
                abbreviation
            FROM metrics
            WHERE
                LOWER(metric_name)
                    LIKE '%' || LOWER(:1) || '%'
                OR
                LOWER(abbreviation)
                    LIKE '%' || LOWER(:2) || '%'
            ORDER BY metric_name
            """,
            [keyword, keyword],
        )
        return cur.fetchall()

    finally:
        cur.close()
        conn.close()
# -------------------------------------------------------------------
# Testing
# -------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 70)
    print("First 10 metrics")
    print("=" * 70)

    for row in get_all_metrics()[:10]:
        print(row)

    print("\n" + "=" * 70)
    print("Search: capital")
    print("=" * 70)

    print(search_metrics("capital"))

    print("\n" + "=" * 70)
    print("Metric ID = 20")
    print("=" * 70)

    print(get_metric_by_id(20)[:3])

    print("\n" + "=" * 70)
    print("CET1")
    print("=" * 70)

    cet1_rows = get_metric_by_name("cet1")
    print(f"Rows returned: {len(cet1_rows)}")

    for row in cet1_rows[:3]:
        print(row)

    print("\n" + "=" * 70)
    print("CET1 Ratio")
    print("=" * 70)

    cet1_ratio_rows = get_metric_by_name("cet1_ratio")
    print(f"Rows returned: {len(cet1_ratio_rows)}")

    for row in cet1_ratio_rows[:3]:
        print(row)

    print("\n" + "=" * 70)
    print("Tier 1")
    print("=" * 70)

    tier1_rows = get_metric_by_name("tier1")
    print(f"Rows returned: {len(tier1_rows)}")

    for row in tier1_rows[:3]:
        print(row)