# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from datetime import datetime
from pathlib import Path

import json
import pandas as pd

# -------------------------------------------------------------------
# Project paths
# -------------------------------------------------------------------

BACKEND_DIR = Path(__file__).resolve().parents[2]

RAW_DIR = BACKEND_DIR / "data" / "raw"
INGESTION_DIR = BACKEND_DIR / "src" / "ingestion"

EXCEL_FILE = RAW_DIR / "260505-1q-2026-data-pack-excel.xlsx"
OUTPUT_FILE = INGESTION_DIR / "scan_sheet_metadata.json"

# -------------------------------------------------------------------
# Sheet Scanner
# -------------------------------------------------------------------

def scan_sheets(path):
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            f"Workbook not found:\n{path}"
        )

    sheet_scan_json = []

    excel = pd.ExcelFile(path)

    for sheet_name in excel.sheet_names:
        sheet_df = excel.parse(sheet_name)

        for row_number, row in sheet_df.iterrows():

            # Skip completely empty rows
            if row.notna().sum() == 0:
                continue

            cleaned_row_values = []

            for value in row.tolist():

                # Convert pandas timestamps to ISO format
                if isinstance(value, (pd.Timestamp, datetime)):
                    value = value.isoformat()

                # Convert NaN / NaT to None
                elif pd.isna(value):
                    value = None

                cleaned_row_values.append(value)

            sheet_scan_json.append({
                "source_workbook": path.name,
                "sheet_name": sheet_name,
                "row_number": int(row_number + 1),
                "row_values": cleaned_row_values,
                "non_null_count": int(row.notna().sum())
            })

    # ---------------------------------------------------------------
    # Write output
    # ---------------------------------------------------------------

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            sheet_scan_json,
            f,
            indent=4,
            ensure_ascii=False
        )

    return sheet_scan_json

# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------

if __name__ == "__main__":
    results = scan_sheets(EXCEL_FILE)

    print("=" * 70)
    print("SHEET SCAN COMPLETE")
    print("=" * 70)

    print(f"Input:  {EXCEL_FILE}")
    print(f"Output: {OUTPUT_FILE}")
    print(f"Rows scanned: {len(results)}")