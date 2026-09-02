from apps.api.engine.rules import normalize_rule_severity
from apps.api.engine.anomaly import normalize_behavior_score
from apps.api.engine.correlation import normalize_correlation_score
from apps.api.engine.impact import normalize_asset_criticality, normalize_business_impact

WEIGHTS = {
    "w_rule": 0.25,
    "w_behavior": 0.20,
    "w_correlation": 0.20,
    "w_criticality": 0.20,
    "w_impact": 0.15
}

def calculate_severity_band(risk_score: float) -> str:
    if risk_score >= 75.0:
        return "CRITICAL"
    elif risk_score >= 50.0:
        return "HIGH"
    elif risk_score >= 25.0:
        return "MEDIUM"
    return "LOW"

def calculate_explainable_risk(
    r_rule: float,
    s_behavior: float,
    c_correlation: float,
    a_criticality: float,
    b_impact: float
) -> dict:
    """
    Computes explainable composite risk score using SentinelEdge Research Risk Model v1.
    All 5 input sub-scores MUST be individually normalized to [0, 100] prior to weighting.
    """
    # Explicit clamp verification on each sub-score
    r = float(min(100.0, max(0.0, r_rule)))
    s = float(min(100.0, max(0.0, s_behavior)))
    c = float(min(100.0, max(0.0, c_correlation)))
    a = float(min(100.0, max(0.0, a_criticality)))
    b = float(min(100.0, max(0.0, b_impact)))

    contrib_rule = WEIGHTS["w_rule"] * r
    contrib_behavior = WEIGHTS["w_behavior"] * s
    contrib_correlation = WEIGHTS["w_correlation"] * c
    contrib_criticality = WEIGHTS["w_criticality"] * a
    contrib_impact = WEIGHTS["w_impact"] * b

    total = contrib_rule + contrib_behavior + contrib_correlation + contrib_criticality + contrib_impact
    composite_risk = float(min(100.0, max(0.0, total)))
    band = calculate_severity_band(composite_risk)

    return {
        "composite_risk_score": round(composite_risk, 1),
        "severity_band": band,
        "r_rule": round(r, 1),
        "s_behavior": round(s, 1),
        "c_correlation": round(c, 1),
        "a_criticality": round(a, 1),
        "b_impact": round(b, 1),
        "weights": WEIGHTS,
        "weighted_contributions": {
            "rule": round(contrib_rule, 2),
            "behavior": round(contrib_behavior, 2),
            "correlation": round(contrib_correlation, 2),
            "criticality": round(contrib_criticality, 2),
            "impact": round(contrib_impact, 2)
        },
        "formula": "Risk = min(100, 0.25*R_rule + 0.20*S_behavior + 0.20*C_correlation + 0.20*A_criticality + 0.15*B_impact)",
        "model_version": "SentinelEdge Research Risk Model v1"
    }
