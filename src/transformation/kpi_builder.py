import json
from datetime import datetime, UTC



def build_kpis(input_file, output_file):

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    kpis = []

    for record in data:

        period_values = record.get("period_values", [])

        latest_value = None
        previous_value = None
        trend = "unknown"

        if len(period_values) >= 1:
            latest_value = period_values[0].get("value")

        if len(period_values) >= 2:
            previous_value = period_values[1].get("value")

        if (
            latest_value is not None
            and previous_value is not None
        ):

            if latest_value > previous_value:
                trend = "up"

            elif latest_value < previous_value:
                trend = "down"

            else:
                trend = "flat"

        kpi_record = {

            "kpi_id":
                f"KPI_{record['metric_id']:04d}",

            "metric_id":
                record["metric_id"],

            "metric_name":
                record["normalized_metric_name"],

            "abbreviation":
                record["abbreviation"],

            "latest_value":
                latest_value,

            "previous_value":
                previous_value,

            "trend":
                trend,

            "business_area":
                record.get("sheet_name"),

            "period_values":
                period_values,

            "source_workbook":
                record.get("source_workbook"),

            "row_number":
                record.get("row_number"),

            "created_at":
              datetime.now(UTC).isoformat()
        }

        kpis.append(kpi_record)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(
            kpis,
            f,
            indent=4
        )

    return kpis


if __name__ == "__main__":

    results = build_kpis(
        "../ingestion/mapped_metrics.json",
        "kpi_records.json"
    )

    print(
        f"Built {len(results)} KPI records"
    )