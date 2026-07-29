# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

import json

from supabase_client import supabase


def load_metrics(input_file):

    with open(input_file, "r", encoding="utf-8") as f:
        records = json.load(f)

    success_count = 0
    failed_count = 0

    for record in records:

        try:

            payload = {
                "metric_id":
                    record.get("metric_id"),

                "metric_name":
                    record.get("normalized_metric_name"),

                "abbreviation":
                    record.get("abbreviation"),

                "period_values":
                    record.get("period_values"),

                "source_workbook":
                    record.get("source_workbook"),

                "sheet_name":
                    record.get("sheet_name"),

                "row_number":
                    record.get("row_number")
            }

            supabase.table( 
             "metrics"
              ).upsert(
                  payload
              ).execute()

            success_count += 1

        except Exception as e:

            failed_count += 1

            print(
                f"Failed metric_id "
                f"{record.get('metric_id')} : {e}"
            )

    print(
        f"\nLoaded: {success_count}"
    )

    print(
        f"Failed: {failed_count}"
    )

    return {
        "loaded": success_count,
        "failed": failed_count
    }


if __name__ == "__main__":

    result = load_metrics(
        "../ingestion/mapped_metrics.json"
    )

    print(result)