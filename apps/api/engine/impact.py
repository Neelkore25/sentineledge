from typing import Optional

CRITICALITY_MAP = {
    "TIER 1 (CROWN JEWEL)": 100.0,
    "TIER 1": 100.0,
    "TIER 2 (HIGH)": 75.0,
    "TIER 2": 75.0,
    "TIER 3 (MEDIUM)": 50.0,
    "TIER 3": 50.0,
    "TIER 4 (LOW)": 25.0,
    "TIER 4": 25.0
}

SENSITIVITY_MAP = {
    "PII / FINANCIAL": 100.0,
    "FINANCIAL": 90.0,
    "PII": 85.0,
    "OPERATIONAL": 60.0,
    "INTERNAL": 40.0,
    "PUBLIC": 10.0
}

def normalize_asset_criticality(criticality_str: str) -> float:
    """Normalizes asset criticality tier string into [0, 100] sub-score A_criticality."""
    return CRITICALITY_MAP.get(criticality_str.upper(), 50.0)

def normalize_business_impact(
    data_sensitivity: str,
    estimated_downtime_cost_per_hour: float,
    user_blast_radius: int
) -> float:
    """
    Normalizes business impact into [0, 100] sub-score B_impact:
    B_impact = clamp[0, 100]( 0.4 * Sensitivity + 0.3 * DowntimeExposure + 0.3 * BlastRadius )
    """
    s_score = SENSITIVITY_MAP.get(data_sensitivity.upper(), 50.0)
    # Scale hourly downtime cost (0 to $10,000/hr -> 0 to 100)
    d_score = min(100.0, (estimated_downtime_cost_per_hour / 10000.0) * 100.0)
    # Scale blast radius (0 to 200 users -> 0 to 100)
    b_score = min(100.0, (user_blast_radius / 200.0) * 100.0)
    
    impact = (0.4 * s_score) + (0.3 * d_score) + (0.3 * b_score)
    return float(min(100.0, max(0.0, impact)))

def calculate_business_impact_tier(b_impact_score: float) -> str:
    if b_impact_score >= 75.0:
        return "CRITICAL"
    elif b_impact_score >= 50.0:
        return "HIGH"
    elif b_impact_score >= 25.0:
        return "MEDIUM"
    return "LOW"
