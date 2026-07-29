# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from warehouse.oracle_client import get_connection


class SQLRetriever:

    def get_metric(self, metric_name: str):

        conn = get_connection()

        try:
            cur = conn.cursor()

            cur.execute(
                """
                SELECT
                    metric_name,
                    abbreviation,
                    period,
                    value
                FROM metrics
                WHERE LOWER(metric_name)=LOWER(:1)
                ORDER BY period
                """,
                [metric_name],
            )

            columns = [col[0].lower() for col in cur.description]

            rows = [
                dict(zip(columns, row))
                for row in cur.fetchall()
            ]

            cur.close()

            return rows

        finally:
            conn.close()