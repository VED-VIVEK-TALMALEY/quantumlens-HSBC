# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

import json
from pathlib import Path

from warehouse.oracle_client import get_connection

BASE_DIR = Path(__file__).resolve().parents[1]

JSON_FILE = (
    BASE_DIR
    / "data"
    / "generated"
    / "kpi_records.json"
)


def load_data():

    conn = get_connection()
    cursor = conn.cursor()

    with open(JSON_FILE, "r", encoding="utf-8") as f:
        records = json.load(f)

    insert_sql = """
    INSERT INTO metrics(
        metric_id,
        metric_name,
        abbreviation,
        sheet_name,
        source_workbook,
        row_number,
        period,
        value,
        unit,
        category
    )
    VALUES(
        :1,:2,:3,:4,:5,:6,:7,:8,:9,:10
    )
    """

    count = 0

    for record in records:

        for period in record["period_values"]:

            cursor.execute(
                insert_sql,
                (
                    record["metric_id"],
                    record["metric_name"],
                    record.get("abbreviation"),
                    record.get("business_area"),
                    record.get("source_workbook"),
                    record.get("row_number"),
                    str(period["period_index"]),
                    period["value"],
                    None,
                    "Financial KPI"
                )
            )

            count += 1

    conn.commit()

    cursor.close()
    conn.close()

    print(f"Loaded {count} rows into Oracle")


if __name__ == "__main__":
    load_data()