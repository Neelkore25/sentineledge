import pytest
from apps.api.engine.rules import (
    BruteForceRule, SuspiciousGeoLoginRule, PrivilegeEscalationRule,
    DataExfiltrationRule, BackupFailureRule, PortScanReconRule,
    evaluate_all_rules, normalize_rule_severity
)

def test_normalize_rule_severity():
    assert normalize_rule_severity("LOW") == 25.0
    assert normalize_rule_severity("MEDIUM") == 50.0
    assert normalize_rule_severity("HIGH") == 75.0
    assert normalize_rule_severity("CRITICAL") == 100.0

def test_brute_force_rule_triggered():
    rule = BruteForceRule(threshold=5)
    events = [
        {"id": f"EV-00{i}", "event_type": "LOGIN_FAILED", "user_id": "admin_user"}
        for i in range(6)
    ]
    result = rule.evaluate(events)
    assert result is not None
    assert result["rule_id"] == "RULE_AUTH_BRUTE_FORCE_001"
    assert result["severity"] == "HIGH"
    assert result["r_rule"] == 75.0
    assert len(result["matched_event_ids"]) == 6

def test_brute_force_rule_not_triggered():
    rule = BruteForceRule(threshold=5)
    events = [
        {"id": f"EV-00{i}", "event_type": "LOGIN_FAILED", "user_id": "admin_user"}
        for i in range(3)
    ]
    result = rule.evaluate(events)
    assert result is None

def test_suspicious_geo_login():
    rule = SuspiciousGeoLoginRule()
    events = [
        {"id": "EV-10", "event_type": "LOGIN_SUCCESS", "location": "Moscow"},
        {"id": "EV-11", "event_type": "LOGIN_SUCCESS", "location": "Mumbai"}
    ]
    result = rule.evaluate(events, allowed_locations=["Mumbai", "Bengaluru"])
    assert result is not None
    assert result["r_rule"] == 50.0
    assert "EV-10" in result["matched_event_ids"]

def test_privilege_escalation_rule():
    rule = PrivilegeEscalationRule()
    events = [
        {"id": "EV-20", "event_type": "PRIVILEGE_CHANGE", "action": "GRANT_ROLE", "endpoint": "/api/v1/admin/roles"}
    ]
    result = rule.evaluate(events)
    assert result is not None
    assert result["severity"] == "CRITICAL"
    assert result["r_rule"] == 100.0

def test_data_exfiltration_rule():
    rule = DataExfiltrationRule(byte_threshold=100 * 1024 * 1024)
    events = [
        {"id": "EV-30", "event_type": "FILE_DOWNLOAD", "bytes_transferred": 200 * 1024 * 1024}
    ]
    result = rule.evaluate(events)
    assert result is not None
    assert result["r_rule"] == 75.0

def test_evaluate_all_rules():
    events = [
        {"id": "EV-01", "event_type": "LOGIN_FAILED"},
        {"id": "EV-02", "event_type": "LOGIN_FAILED"},
        {"id": "EV-03", "event_type": "LOGIN_FAILED"},
        {"id": "EV-04", "event_type": "LOGIN_FAILED"},
        {"id": "EV-05", "event_type": "LOGIN_FAILED"},
        {"id": "EV-06", "event_type": "PRIVILEGE_CHANGE"}
    ]
    matches = evaluate_all_rules(events)
    assert len(matches) >= 2
    rule_ids = [m["rule_id"] for m in matches]
    assert "RULE_AUTH_BRUTE_FORCE_001" in rule_ids
    assert "RULE_PRIV_ESCALATION_003" in rule_ids
