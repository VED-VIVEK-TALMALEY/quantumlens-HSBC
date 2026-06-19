import json

def value_extractor(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = []
    for row in data:
        numeric_values = [
            v for v in row.get("row_values", [])
            if isinstance(v, (int, float))
        ]
        results.append({
            "metric_id": row["metric_id"],
            "normalized_metric_name": row["normalized_metric_name"],
            "abbreviation": row["abbreviation"],
            "sheet_name": row.get("sheet_name", ""),
            "numeric_values": numeric_values
        })

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    return results

results1 = value_extractor(
    extracted_metric.json,
    valued_metrics.json
)
print(json.dumps(results1[:3], indent=2))