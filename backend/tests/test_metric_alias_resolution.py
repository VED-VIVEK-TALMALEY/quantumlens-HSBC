from warehouse.query_service import resolve_metric_name

def test_resolve_known_metric_aliases():
    assert resolve_metric_name(" CET1 ") == ["common_equity_tier_1_capital", "cet1"]
    assert resolve_metric_name("pbt") == ["profit_before_tax", "pbt"]
    assert resolve_metric_name("profit_before_tax") == ["profit_before_tax", "pbt"]
    assert resolve_metric_name("CET1R") == ["common_equity_tier_1_ratio", "cet1_ratio", "cet1r"]

def test_unknown_metric_is_preserved():
    assert resolve_metric_name("custom_metric") == ["custom_metric"]

def test_empty_metric_is_empty():
    assert resolve_metric_name(" ") == []
