import json

def value_extractor(input_file, output_file):

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = []

    for row in data:

        numeric_values = [
            value
            for value in row.get("row_values", [])
            if isinstance(value, (int, float))
        ]

        results.append({
            "metric_id": row["metric_id"],
            "normalized_metric_name": row["normalized_metric_name"],
            "abbreviation": row["abbreviation"],
            "numeric_values": numeric_values,
            "numeric_count": len(numeric_values),

            "source_workbook": row.get("source_workbook"),
            "sheet_name": row.get("sheet_name"),
            "row_number": row.get("row_number")
        })

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    return results


results = value_extractor(
    "extracted_metrics.json",
    "valued_metrics.json"
)

print(json.dumps(results, indent=4))