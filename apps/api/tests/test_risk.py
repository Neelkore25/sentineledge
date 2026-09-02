import pytest
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
