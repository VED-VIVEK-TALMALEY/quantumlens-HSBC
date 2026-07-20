import json

def period_mapper(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    mapped_records = []

    for row in data:

        numeric_values = row.get("numeric_values", [])

        period_values = []

        for idx, value in enumerate(numeric_values):
            period_values.append({
                "period_index": idx + 1,
                "value": value
            })

        mapped_records.append({
            "metric_id": row["metric_id"],
            "normalized_metric_name":
                row["normalized_metric_name"],
            "abbreviation":
                row["abbreviation"],

            "period_values":
                period_values,

            "source_workbook":
                row.get("source_workbook"),

            "sheet_name":
                row.get("sheet_name"),

            "row_number":
                row.get("row_number")
        })

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(mapped_records, f, indent=4)

    return mapped_records


results = period_mapper(
    "valued_metrics.json",
    "mapped_metrics.json"
)

print(f"Mapped Records: {len(results)}")