import json


def load_kpi_catalog(path="metric_dictionary.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_metrics(
    input_file,
    output_file,
    catalog_path="metric_dictionary.json"
):
    catalog = load_kpi_catalog(catalog_path)

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    extracted_data = []

    for entry in data:

        row = entry.get("row_values", [])

        # Get all text cells from the row
        text_cells = [
            str(cell).lower().strip()
            for cell in row
            if isinstance(cell, str)
        ]

        matched_text = None
        matched_kpi = None

        # First match wins
        for text in text_cells:

            kpi_data = catalog.get(text)

            if kpi_data:
                matched_text = text
                matched_kpi = kpi_data
                break

        if matched_kpi:

            extracted_data.append({
                "metric_id": matched_kpi["metric_id"],
                "matched_text": matched_text,
                "normalized_metric_name":
                    matched_kpi["normalized_metric_name"],
                "abbreviation":
                    matched_kpi["abbreviation"],

                # Preserve original row for later value extraction
                "row_values": row,

                "source_workbook":
                    entry.get("source_workbook"),

                "sheet_name":
                    entry.get("sheet_name"),

                "row_number":
                    entry.get("row_number")
            })

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(extracted_data, f, indent=4)

    return extracted_data


results = extract_metrics(
    "scan_sheet_metadata.json",
    "extracted_metrics.json"
)
print(len(results))
