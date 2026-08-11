# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

import json
from pathlib import Path

# -------------------------------------------------------------------
# Paths
# -------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DEFAULT_CATALOG = BASE_DIR / "metric_dictionary.json"
DEFAULT_INPUT = BASE_DIR / "scan_sheet_metadata.json"
DEFAULT_OUTPUT = BASE_DIR / "extracted_metrics.json"

# -------------------------------------------------------------------
# Load KPI catalog
# -------------------------------------------------------------------

def load_kpi_catalog(path=DEFAULT_CATALOG):
    path = Path(path)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# -------------------------------------------------------------------
# Extract metrics
# -------------------------------------------------------------------

def extract_metrics(
    input_file=DEFAULT_INPUT,
    output_file=DEFAULT_OUTPUT,
    catalog_path=DEFAULT_CATALOG
):
    input_file = Path(input_file)
    output_file = Path(output_file)
    catalog_path = Path(catalog_path)

    catalog = load_kpi_catalog(catalog_path)

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    extracted_data = []

    for entry in data:
        row = entry.get("row_values", [])

        # ------------------------------------------------------------
        # Get all text cells from the row
        # ------------------------------------------------------------

        text_cells = [
            str(cell).lower().strip()
            for cell in row
            if isinstance(cell, str)
        ]

        matched_text = None
        matched_kpi = None

        # ------------------------------------------------------------
        # First catalog match wins
        # ------------------------------------------------------------

        for text in text_cells:
            kpi_data = catalog.get(text)

            if kpi_data:
                matched_text = text
                matched_kpi = kpi_data
                break

        # ------------------------------------------------------------
        # Store matched metric
        # ------------------------------------------------------------

        if matched_kpi:
            extracted_data.append(
                {
                    "metric_id": matched_kpi["metric_id"],
                    "matched_text": matched_text,
                    "normalized_metric_name": matched_kpi["normalized_metric_name"],
                    "abbreviation": matched_kpi["abbreviation"],
                    # Preserve original row for value extraction
                    "row_values": row,
                    "source_workbook": entry.get("source_workbook"),
                    "sheet_name": entry.get("sheet_name"),
                    "row_number": entry.get("row_number"),
                }
            )

    # ------------------------------------------------------------
    # Write output
    # ------------------------------------------------------------

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(
            extracted_data,
            f,
            indent=4,
            ensure_ascii=False
        )

    return extracted_data

# -------------------------------------------------------------------
# Testing
# -------------------------------------------------------------------

if __name__ == "__main__":
    results = extract_metrics()

    print("=" * 70)
    print("METRIC EXTRACTION COMPLETE")
    print("=" * 70)

    print(f"Input:   {DEFAULT_INPUT}")
    print(f"Catalog: {DEFAULT_CATALOG}")
    print(f"Output:  {DEFAULT_OUTPUT}")
    print(f"Metrics extracted: {len(results)}")