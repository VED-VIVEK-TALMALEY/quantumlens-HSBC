# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from warehouse.oracle_client import get_connection


class MetricRepository:

    def get_all_metrics(self):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT DISTINCT
                metric_id,
                metric_name,
                abbreviation
            FROM metrics
            ORDER BY metric_id
        """)

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows

    def get_metric(self, metric_id: int):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM metrics
            WHERE metric_id = :id
        """, {"id": metric_id})

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows

    def search_metric(self, name: str):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT DISTINCT
                metric_id,
                metric_name,
                abbreviation
            FROM metrics
            WHERE LOWER(metric_name)
            LIKE LOWER(:name)
        """, {
            "name": f"%{name}%"
        })

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows

    def get_latest_value(self, metric_id: int):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT value
            FROM metrics
            WHERE metric_id = :id
            ORDER BY row_number DESC
            FETCH FIRST 1 ROW ONLY
        """, {"id": metric_id})

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        return row