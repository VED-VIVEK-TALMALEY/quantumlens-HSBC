from warehouse.oracle_client import get_connection


def get_all_metrics():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
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

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


if __name__ == "__main__":

    for row in get_all_metrics()[:10]:
        print(row)