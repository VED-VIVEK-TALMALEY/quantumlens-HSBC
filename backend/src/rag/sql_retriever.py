from warehouse.oracle_client import get_connection


class SQLRetriever:

    def get_metric(self, metric_name: str):

        conn = get_connection()

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
            [metric_name]
        )

        rows = cur.fetchall()

        cur.close()
        conn.close()

        return rows