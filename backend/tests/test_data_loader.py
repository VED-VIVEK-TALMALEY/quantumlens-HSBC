import json
import pytest
from warehouse.data_loader import read_and_validate, to_supabase_payload

def test_canonical_source_contains_pbt():
    from warehouse.data_loader import DEFAULT_INPUT
    rows = read_and_validate(DEFAULT_INPUT)
    assert len(rows) == 456
    assert sum(r.get("metric_id") == 7 for r in rows) == 90

def test_payload_maps_canonical_fields():
    payload = to_supabase_payload({
        "metric_id": 7, "normalized_metric_name": "profit_before_tax", "abbreviation": "pbt",
        "period_values": [{"period_index": 1, "period_label": "Period 1", "value": 9376}],
        "source_workbook": "source.xlsx", "sheet_name": "Group income statement", "row_number": 13,
    })
    assert payload["metric_name"] == "profit_before_tax"
    assert payload["abbreviation"] == "pbt"
    assert payload["row_number"] == 13

def test_duplicate_source_keys_are_rejected(tmp_path):
    path = tmp_path / "mapped.json"
    record = {"metric_id": 7, "normalized_metric_name": "profit_before_tax", "abbreviation": "pbt", "period_values": [], "sheet_name": "Group income statement", "row_number": 13}
    path.write_text(json.dumps([record, record]), encoding="utf-8")
    with pytest.raises(ValueError, match="Duplicate source record key"):
        read_and_validate(path)
