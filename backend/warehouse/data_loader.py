"""Idempotent Supabase loader for the canonical mapped KPI dataset.

Canonical input: backend/src/ingestion/mapped_metrics.json
Before writing, --apply snapshots the existing metrics table to backend/data/backups/.
Rows are keyed by the existing unique constraint (metric_id, sheet_name, row_number).
"""
from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BACKEND_DIR = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = BACKEND_DIR / "src" / "ingestion" / "mapped_metrics.json"
GENERATED_COPY = BACKEND_DIR / "data" / "generated" / "mapped_metrics.json"
BACKUP_DIR = BACKEND_DIR / "data" / "backups"
BATCH_SIZE = 100
CONFLICT_COLUMNS = "metric_id,sheet_name,row_number"
REQUIRED_FIELDS = ("metric_id", "normalized_metric_name", "sheet_name", "row_number")


def read_and_validate(input_file: str | Path = DEFAULT_INPUT) -> list[dict[str, Any]]:
    path = Path(input_file).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"Mapped KPI source not found: {path}")
    with path.open("r", encoding="utf-8-sig") as handle:
        records = json.load(handle)
    if not isinstance(records, list) or not records:
        raise ValueError(f"Expected a non-empty JSON list in {path}")

    seen: set[tuple[Any, Any, Any]] = set()
    cleaned: list[dict[str, Any]] = []
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError(f"Record {index} is not an object")
        missing = [field for field in REQUIRED_FIELDS if record.get(field) is None]
        if missing:
            raise ValueError(f"Record {index} missing required fields: {', '.join(missing)}")
        key = (record["metric_id"], record["sheet_name"], record["row_number"])
        if key in seen:
            raise ValueError(f"Duplicate source record key at record {index}: {key}")
        seen.add(key)
        if not isinstance(record.get("period_values", []), list):
            raise ValueError(f"Record {index} period_values must be a list")
        cleaned.append(record)
    return cleaned


def to_supabase_payload(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "metric_id": record["metric_id"],
        "metric_name": record["normalized_metric_name"],
        "abbreviation": record.get("abbreviation") or "",
        "period_values": record.get("period_values") or [],
        "source_workbook": record.get("source_workbook"),
        "sheet_name": record["sheet_name"],
        "row_number": record["row_number"],
    }


def backup_current_table(client) -> Path:
    """Export all existing metric rows before any upsert; paginates safely."""
    rows: list[dict[str, Any]] = []
    start = 0
    page_size = 1000
    while True:
        response = (
            client.table("metrics").select("*")
            .range(start, start + page_size - 1).execute()
        )
        page = response.data or []
        rows.extend(page)
        if len(page) < page_size:
            break
        start += page_size

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_path = BACKUP_DIR / f"metrics_before_load_{stamp}.json"
    with backup_path.open("w", encoding="utf-8") as handle:
        json.dump(rows, handle, indent=2, ensure_ascii=False)
    return backup_path


def load_metrics(input_file: str | Path = DEFAULT_INPUT, *, apply: bool = False) -> dict[str, Any]:
    records = read_and_validate(input_file)
    payloads = [to_supabase_payload(record) for record in records]
    pbt_count = sum(1 for record in records if record.get("metric_id") == 7 or record.get("normalized_metric_name") == "profit_before_tax")
    summary: dict[str, Any] = {
        "source": str(Path(input_file).resolve()),
        "source_records": len(records),
        "source_pbt_records": pbt_count,
        "apply": apply,
        "loaded": 0,
        "failed": 0,
        "backup": None,
    }
    if not apply:
        print(json.dumps(summary, indent=2))
        print("Dry run only. Re-run with --apply to back up the current table and upsert records.")
        return summary

    # Lazy import means source validation and unit tests do not need live credentials.
    from warehouse.supabase_client import get_supabase
    client = get_supabase()

    backup_path = backup_current_table(client)
    summary["backup"] = str(backup_path)
    print(f"Existing metrics table backed up to: {backup_path}")

    for start in range(0, len(payloads), BATCH_SIZE):
        batch = payloads[start:start + BATCH_SIZE]
        response = (
            client.table("metrics")
            .upsert(batch, on_conflict=CONFLICT_COLUMNS)
            .execute()
        )
        # A successful PostgREST request raises on error; record response size for progress.
        summary["loaded"] += len(response.data or batch)
        print(f"Upserted {min(start + len(batch), len(payloads))}/{len(payloads)} records")

    # Verify PBT specifically before syncing the generated mirror.
    pbt_response = (
        client.table("metrics").select("id,metric_id,metric_name,abbreviation")
        .eq("metric_id", 7).execute()
    )
    pbt_rows = pbt_response.data or []
    if len(pbt_rows) != pbt_count:
        raise RuntimeError(
            f"Load completed but PBT verification mismatch: source={pbt_count}, database={len(pbt_rows)}. "
            f"Backup retained at {backup_path}."
        )

    GENERATED_COPY.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(input_file).resolve(), GENERATED_COPY)
    summary["database_pbt_records"] = len(pbt_rows)
    summary["generated_copy"] = str(GENERATED_COPY)
    print(json.dumps(summary, indent=2))
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Load canonical mapped KPI records into Supabase")
    parser.add_argument("--input", default=str(DEFAULT_INPUT), help="Mapped JSON input path")
    parser.add_argument("--apply", action="store_true", help="Back up the current table, then upsert")
    args = parser.parse_args()
    load_metrics(args.input, apply=args.apply)


if __name__ == "__main__":
    main()
