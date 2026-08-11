## -------------------------------------------------------------------
## Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
## This project and its source code are strictly proprietary.
## Unauthorized copying, distribution, or use is strictly prohibited.
## -------------------------------------------------------------------

import json
from pathlib import Path


def period_mapper(input_file, output_file):
    """
    Map numeric metric values into structured period records.

    Important:
    - Preserves period_index.
    - Preserves period_label when available.
    - Does NOT invent period labels.
    - Falls back to the numeric period index when labels are unavailable.
    """

    input_path = Path(input_file)
    output_path = Path(output_file)

    if not input_path.exists():

        raise FileNotFoundError(
            f"Input file not found: {input_path.resolve()}"
        )

    with input_path.open("r", encoding="utf-8") as f:

        data = json.load(f)

    mapped_records = []

    for row in data:

        numeric_values = row.get("numeric_values", [])

        # ------------------------------------------------------------
        # Try to preserve period labels if they already exist in the
        # upstream extraction output.
        #
        # Supported possibilities:
        #   period_labels
        #   periods
        # ------------------------------------------------------------

        period_labels = (
            row.get("period_labels")
            or row.get("periods")
            or []
        )

        period_values = []

        for idx, value in enumerate(numeric_values):

            period_record = {
                "period_index": idx + 1,
                "value": value
            }

            # --------------------------------------------------------
            # Preserve actual period label when available.
            # --------------------------------------------------------

            if idx < len(period_labels):

                period_record["period_label"] = str(
                    period_labels[idx]
                )

            else:

                # ----------------------------------------------------
                # Do not pretend that "1" means "1Q26".
                # Keep an explicit fallback label so downstream
                # systems know that this is an unresolved period.
                # ----------------------------------------------------

                period_record["period_label"] = f"Period {idx + 1}"

            period_values.append(period_record)

        mapped_records.append({

            "metric_id":
                row["metric_id"],

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

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with output_path.open("w", encoding="utf-8") as f:

        json.dump(
            mapped_records,
            f,
            indent=4,
            ensure_ascii=False
        )

    return mapped_records


# -------------------------------------------------------------------
# Testing
# -------------------------------------------------------------------

if __name__ == "__main__":

    BASE_DIR = Path(__file__).resolve().parent

    input_file = (
        BASE_DIR.parent
        / "ingestion"
        / "valued_metrics.json"
    )

    output_file = (
        BASE_DIR.parent
        / "ingestion"
        / "mapped_metrics.json"
    )

    results = period_mapper(
        input_file,
        output_file
    )

    print(
        f"Mapped Records: {len(results)}"
    )

    print(
        f"Input:  {input_file}"
    )

    print(
        f"Output: {output_file}"
    )