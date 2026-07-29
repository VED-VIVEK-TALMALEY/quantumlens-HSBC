# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from warehouse.oracle_client import get_connection


def get_all_metrics():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
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
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows


def get_metric_by_id(metric_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM metrics
        WHERE metric_id = :1
        ORDER BY period
    """, [metric_id])

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows


def get_metric_by_name(metric):

    conn = get_connection()
    cur = conn.cursor()

    metric = metric.lower()

    cur.execute("""
SELECT *
FROM metrics
WHERE LOWER(metric_name)=LOWER(:metric)
   OR LOWER(abbreviation)=LOWER(:metric)
ORDER BY period
""", {"metric": metric})
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows


def search_metrics(keyword):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT DISTINCT
            metric_id,
            metric_name,
            abbreviation
        FROM metrics
        WHERE LOWER(metric_name) LIKE '%' || LOWER(:1) || '%'
        ORDER BY metric_name
    """, [keyword])

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows


if __name__ == "__main__":

    print("First 10 metrics")
    for row in get_all_metrics()[:10]:
        print(row)

    print("\nSearch: capital")
    print(search_metrics("capital"))

    print("\nMetric ID = 20")
    print(get_metric_by_id(20)[:3])

    print("\nMetric Name = net_interest_income")
    print(get_metric_by_name("net_interest_income")[:3])