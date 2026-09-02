import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

write_file("apps/api/tests/__init__.py", "# Tests module\n")

# 1. Test Rules
write_file("apps/api/tests/test_rules.py", """import pytest
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
""")

# 2. Test Anomaly
write_file("apps/api/tests/test_anomaly.py", """import pytest
import numpy as np
from apps.api.engine.anomaly import (
    calculate_mad, robust_z_score, normalize_behavior_score, evaluate_user_behavior
)

def test_calculate_mad():
    data = [40.0, 42.0, 45.0, 48.0, 44.0, 46.0, 43.0]
    median, mad = calculate_mad(data)
    assert median == 44.0
    assert mad > 0.0

def test_robust_z_score_normal():
    data = [40.0, 42.0, 45.0, 48.0, 44.0, 46.0, 43.0]
    z = robust_z_score(45.0, data)
    assert z < 1.0
    s_score = normalize_behavior_score(z)
    assert s_score < 30.0

def test_robust_z_score_extreme_anomaly():
    data = [40.0, 42.0, 45.0, 48.0, 44.0, 46.0, 43.0]
    # 2.4 GB observed vs 45 MB baseline
    z = robust_z_score(2400.0, data)
    assert z > 10.0
    s_score = normalize_behavior_score(z)
    assert s_score == 100.0 # Clamped to 100 max

def test_evaluate_user_behavior_combined():
    user_baseline = {
        "download_history_json": [40.0, 42.0, 45.0, 48.0, 44.0, 46.0, 43.0],
        "typical_login_start_hour": 9,
        "typical_login_end_hour": 18
    }
    # Anomaly: 1.5 GB download at 03:00 AM (night)
    res = evaluate_user_behavior(
        observed_download_mb=1500.0,
        observed_login_hour=3,
        user_baseline=user_baseline
    )
    assert res["s_behavior"] >= 75.0
    assert res["z_mad_download"] > 5.0
    assert 0.0 <= res["s_behavior"] <= 100.0
""")

# 3. Test Correlation
write_file("apps/api/tests/test_correlation.py", """import pytest
from apps.api.engine.correlation import EventCorrelator, normalize_correlation_score

def test_normalize_correlation_score_clamping():
    assert normalize_correlation_score(1, 1) == 30.0
    assert normalize_correlation_score(5, 3) == 100.0 # 50 + 60 = 110 -> 100.0
    assert normalize_correlation_score(0, 0) == 0.0

def test_event_correlator_window():
    correlator = EventCorrelator(window_minutes=30)
    events = [
        {"id": "EV-01", "user_id": "finance_admin", "event_type": "LOGIN_FAILED"},
        {"id": "EV-02", "user_id": "finance_admin", "event_type": "LOGIN_SUCCESS"},
        {"id": "EV-03", "user_id": "finance_admin", "event_type": "ADMIN_ACCESS", "action": "GRANT_ROLE"},
        {"id": "EV-04", "user_id": "finance_admin", "event_type": "FILE_DOWNLOAD", "bytes_transferred": 50_000_000}
    ]
    res = correlator.correlate_events(events, target_user="finance_admin")
    assert res["event_count"] == 4
    assert res["stage_diversity"] >= 3
    assert res["c_correlation"] >= 80.0
    assert len(res["correlated_event_ids"]) == 4

def test_event_correlator_empty():
    correlator = EventCorrelator(window_minutes=30)
    res = correlator.correlate_events([], target_user="finance_admin")
    assert res["event_count"] == 0
    assert res["c_correlation"] == 0.0
""")

# 4. Test Risk Model
write_file("apps/api/tests/test_risk.py", """import pytest
from apps.api.engine.risk import calculate_explainable_risk, calculate_severity_band, WEIGHTS

def test_risk_weights_sum_to_one():
    total_weights = sum(WEIGHTS.values())
    assert abs(total_weights - 1.0) < 1e-6

def test_calculate_severity_bands():
    assert calculate_severity_band(15.0) == "LOW"
    assert calculate_severity_band(35.0) == "MEDIUM"
    assert calculate_severity_band(65.0) == "HIGH"
    assert calculate_severity_band(85.0) == "CRITICAL"

def test_explainable_risk_calculation():
    # R_rule=75 (High), S_behavior=80 (Anomalous), C_correlation=70, A_criticality=100 (Tier 1), B_impact=85
    res = calculate_explainable_risk(
        r_rule=75.0,
        s_behavior=80.0,
        c_correlation=70.0,
        a_criticality=100.0,
        b_impact=85.0
    )
    # Expected: 0.25*75 + 0.20*80 + 0.20*70 + 0.20*100 + 0.15*85
    # = 18.75 + 16.0 + 14.0 + 20.0 + 12.75 = 81.5
    assert res["composite_risk_score"] == 81.5
    assert res["severity_band"] == "CRITICAL"
    assert res["r_rule"] == 75.0
    assert res["s_behavior"] == 80.0
    assert res["c_correlation"] == 70.0
    assert res["a_criticality"] == 100.0
    assert res["b_impact"] == 85.0
    assert res["weighted_contributions"]["rule"] == 18.75
    assert res["weighted_contributions"]["criticality"] == 20.0

def test_risk_clamping_boundary():
    # Extreme inputs beyond 100 must be clamped
    res = calculate_explainable_risk(
        r_rule=150.0,
        s_behavior=200.0,
        c_correlation=120.0,
        a_criticality=100.0,
        b_impact=100.0
    )
    assert res["composite_risk_score"] == 100.0
    assert res["r_rule"] == 100.0
    assert res["s_behavior"] == 100.0
""")

# 5. Test Recovery Readiness
write_file("apps/api/tests/test_recovery.py", """import pytest
from apps.api.engine.recovery import calculate_recovery_readiness

def test_recovery_readiness_healthy():
    res = calculate_recovery_readiness(
        backup_freshness_hours=2.0,
        target_rpo_hours=4.0,
        verified=True,
        last_test_days_ago=15.0,
        rto_actual_hours=2.5,
        rto_target_hours=4.0
    )
    assert res["readiness_index"] == 100.0
    assert res["rpo_gap_hours"] == 0.0
    assert res["b_freshness"] == 100.0
    assert res["v_verified"] == 100.0
    assert res["t_recency"] == 100.0

def test_recovery_readiness_degraded_unverified():
    res = calculate_recovery_readiness(
        backup_freshness_hours=18.0,
        target_rpo_hours=4.0,
        verified=False,
        last_test_days_ago=75.0,
        rto_actual_hours=6.0,
        rto_target_hours=4.0
    )
    assert res["readiness_index"] < 60.0
    assert res["rpo_gap_hours"] == 14.0
    assert res["v_verified"] == 0.0
    assert "Last snapshot backup has not been verified" in res["primary_weakness"]
""")

print("Phase 1 test suite written!")
