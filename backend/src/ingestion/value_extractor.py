## -------------------------------------------------------------------
## Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
## This project and its source code are strictly proprietary.
## Unauthorized copying, distribution, or use is strictly prohibited.
## -------------------------------------------------------------------

import json
from pathlib import Path


def value_extractor(input_file, output_file):
    """
    Extract numeric values from extracted metric records.

    Input:
        extracted_metrics.json

    Output:
        valued_metrics.json
    """

    input_path = Path(input_file)
    output_path = Path(output_file)

    if not input_path.exists():

        raise FileNotFoundError(
            f"Input file not found: {input_path.resolve()}"
        )

    with input_path.open("r", encoding="utf-8") as f:

        data = json.load(f)

    results = []

    for row in data:

        numeric_values = [
            value
            for value in row.get("row_values", [])
            if isinstance(value, (int, float))
            and not isinstance(value, bool)
        ]

        results.append(
            {
                "metric_id":
                    row["metric_id"],

                "normalized_metric_name":
                    row["normalized_metric_name"],

                "abbreviation":
                    row["abbreviation"],

                "numeric_values":
                    numeric_values,

                "numeric_count":
                    len(numeric_values),

                "source_workbook":
                    row.get("source_workbook"),

                "sheet_name":
                    row.get("sheet_name"),

                "row_number":
                    row.get("row_number"),
            }
        )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with output_path.open("w", encoding="utf-8") as f:

        json.dump(
            results,
            f,
            indent=4,
            ensure_ascii=False
        )

    return results


# -------------------------------------------------------------------
# Testing
# -------------------------------------------------------------------

if __name__ == "__main__":

    current_dir = Path(__file__).resolve().parent

    input_file = current_dir / "../ingestion/extracted_metrics.json"
    output_file = current_dir / "../ingestion/valued_metrics.json"

    results = value_extractor(
        input_file,
        output_file
    )

    print("=" * 70)
    print("VALUE EXTRACTION COMPLETE")
    print("=" * 70)
    print(f"Input : {input_file.resolve()}")
    print(f"Output: {output_file.resolve()}")
    print(f"Records: {len(results)}")
    print("=" * 70)