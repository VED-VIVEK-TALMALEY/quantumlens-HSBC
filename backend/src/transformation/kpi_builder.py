# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
#
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

import json
from datetime import datetime, UTC


# -------------------------------------------------------------------
# KPI Builder
# -------------------------------------------------------------------

def build_kpis(input_file, output_file):
    """
    Build normalized KPI records from mapped metric records.

    Important:
    - Preserves source period labels.
    - Preserves business area, sheet, and source row.
    - Period 1 is the latest period in the current HSBC ingestion model.
    - Period 2 is the previous period.
    - Does not invent, aggregate, or modify source values.
    - One KPI record is produced for each mapped source record.
    """

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    kpis = []

    for record in data:

        metric_id = record.get("metric_id")
        metric_name = record.get("normalized_metric_name")
        abbreviation = record.get("abbreviation")

        # ------------------------------------------------------------
        # Validate required fields
        # ------------------------------------------------------------

        if metric_id is None:
            continue

        if not metric_name:
            continue

        if not abbreviation:
            abbreviation = ""

        # ------------------------------------------------------------
        # Normalize period values
        # ------------------------------------------------------------

        source_period_values = record.get("period_values", [])

        normalized_period_values = []

        for index, period in enumerate(source_period_values):

            if not isinstance(period, dict):
                continue

            period_index = period.get(
                "period_index",
                index + 1
            )

            period_label = period.get(
                "period_label",
                f"Period {period_index}"
            )

            value = period.get("value")

            normalized_period_values.append({
                "period_index": period_index,
                "period_label": period_label,
                "value": value,
            })

        # ------------------------------------------------------------
        # Ensure period ordering is deterministic.
        #
        # Current HSBC model:
        # Period 1 = latest
        # Period 2 = previous
        # ------------------------------------------------------------

        normalized_period_values.sort(
            key=lambda x: x["period_index"]
        )

        # ------------------------------------------------------------
        # Latest / previous values
        # ------------------------------------------------------------

        latest_period = (
            normalized_period_values[0]
            if len(normalized_period_values) >= 1
            else None
        )

        previous_period = (
            normalized_period_values[1]
            if len(normalized_period_values) >= 2
            else None
        )

        latest_value = (
            latest_period["value"]
            if latest_period
            else None
        )

        previous_value = (
            previous_period["value"]
            if previous_period
            else None
        )

        # ------------------------------------------------------------
        # Determine trend
        # ------------------------------------------------------------

        trend = "unknown"

        if (
            latest_value is not None
            and previous_value is not None
        ):
            try:
                latest_numeric = float(latest_value)
                previous_numeric = float(previous_value)

                if latest_numeric > previous_numeric:
                    trend = "up"

                elif latest_numeric < previous_numeric:
                    trend = "down"

                else:
                    trend = "flat"

            except (TypeError, ValueError):
                trend = "unknown"

        # ------------------------------------------------------------
        # KPI ID
        #
        # metric_id alone is NOT enough to uniquely identify a KPI
        # because the same metric can exist across multiple sheets.
        #
        # Therefore include the source row in the KPI identifier.
        # ------------------------------------------------------------

        sheet_name = record.get("sheet_name", "")
        row_number = record.get("row_number", "")

        kpi_id = (
            f"KPI_{metric_id:04d}"
            f"_{str(sheet_name).replace(' ', '_')}"
            f"_{row_number}"
        )

        # ------------------------------------------------------------
        # Build KPI record
        # ------------------------------------------------------------

        kpi_record = {
            "kpi_id": kpi_id,

            "metric_id": metric_id,

            "metric_name": metric_name,

            "abbreviation": abbreviation,

            "latest_value": latest_value,

            "latest_period": (
                latest_period["period_label"]
                if latest_period
                else None
            ),

            "previous_value": previous_value,

            "previous_period": (
                previous_period["period_label"]
                if previous_period
                else None
            ),

            "trend": trend,

            "business_area": sheet_name,

            "period_values": normalized_period_values,

            "source_workbook": record.get(
                "source_workbook"
            ),

            "sheet_name": sheet_name,

            "row_number": row_number,

            "created_at": datetime.now(
                UTC
            ).isoformat(),
        }

        kpis.append(kpi_record)

    # ---------------------------------------------------------------
    # Write output
    # ---------------------------------------------------------------

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            kpis,
            f,
            indent=4,
            ensure_ascii=False
        )

    return kpis


# -------------------------------------------------------------------
# Testing
# -------------------------------------------------------------------

if __name__ == "__main__":

    results = build_kpis(
        "src/ingestion/mapped_metrics.json",
        "src/ingestion/kpi_records.json",
    )

    print("=" * 70)
    print("KPI BUILD COMPLETE")
    print("=" * 70)

    print(
        f"Mapped records: "
        f"{len(results)}"
    )

    # ---------------------------------------------------------------
    # Diagnostic counts
    # ---------------------------------------------------------------

    pbt_records = [
        record
        for record in results
        if record.get("metric_name")
        == "profit_before_tax"
    ]

    nii_records = [
        record
        for record in results
        if record.get("metric_name")
        == "net_interest_income"
    ]

    print(
        f"PBT KPI records: "
        f"{len(pbt_records)}"
    )

    print(
        f"NII KPI records: "
        f"{len(nii_records)}"
    )

    # ---------------------------------------------------------------
    # Show first PBT record for verification
    # ---------------------------------------------------------------

    if pbt_records:

        print("\nFirst PBT KPI:")
        print(
            json.dumps(
                pbt_records[0],
                indent=4,
                ensure_ascii=False
            )
        )

    else:

        print(
            "\nWARNING: No PBT KPI records were built."
        )