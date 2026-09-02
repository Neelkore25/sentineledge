from datetime import datetime, timezone, timedelta

def calculate_recovery_readiness(
    backup_freshness_hours: float,
    target_rpo_hours: float,
    verified: bool,
    last_test_days_ago: float,
    rto_actual_hours: float,
    rto_target_hours: float
) -> dict:
    """
    Calculates Recovery Readiness Index:
    Readiness = 0.35 * B_freshness + 0.25 * V_verified + 0.20 * T_test_recency + 0.20 * R_compliance
    All sub-factors are normalized in [0, 100].
    """
    # 1. Freshness Score (100 if within RPO target, decays linearly up to 3x RPO)
    rpo_gap_hours = max(0.0, backup_freshness_hours - target_rpo_hours)
    if backup_freshness_hours <= target_rpo_hours:
        b_freshness = 100.0
    else:
        overage = backup_freshness_hours - target_rpo_hours
        b_freshness = max(0.0, 100.0 - (overage / target_rpo_hours) * 50.0)

    # 2. Verification Score
    v_verified = 100.0 if verified else 0.0

    # 3. Recovery Drill Recency Score (100 if tested <= 30 days ago, 0 if > 90 days ago)
    if last_test_days_ago <= 30.0:
        t_recency = 100.0
    elif last_test_days_ago >= 90.0:
        t_recency = max(0.0, 20.0 - (last_test_days_ago - 90.0) * 0.5)
    else:
        t_recency = 100.0 - ((last_test_days_ago - 30.0) / 60.0) * 80.0

    # 4. RTO / RPO SLA Compliance Score
    rto_ratio = rto_actual_hours / max(0.1, rto_target_hours)
    if rto_ratio <= 1.0:
        r_compliance = 100.0
    else:
        r_compliance = max(0.0, 100.0 - (rto_ratio - 1.0) * 100.0)

    # Composite Index
    readiness_index = (0.35 * b_freshness) + (0.25 * v_verified) + (0.20 * t_recency) + (0.20 * r_compliance)
    readiness_index = float(min(100.0, max(0.0, readiness_index)))

    # Determine primary recovery weakness
    weaknesses = []
    if not verified:
        weaknesses.append("Last snapshot backup has not been verified.")
    if rpo_gap_hours > 0:
        weaknesses.append(f"Backup freshness exceeds target RPO by {rpo_gap_hours:.1f} hours.")
    if last_test_days_ago > 45:
        weaknesses.append(f"Recovery drill is overdue (last tested {int(last_test_days_ago)} days ago).")
    if rto_actual_hours > rto_target_hours:
        weaknesses.append(f"Actual restoration time ({rto_actual_hours:.1f}h) exceeds SLA ({rto_target_hours:.1f}h).")
    
    primary_weakness = weaknesses[0] if weaknesses else "All recovery parameters within target SLAs."

    return {
        "readiness_index": round(readiness_index, 1),
        "b_freshness": round(b_freshness, 1),
        "v_verified": round(v_verified, 1),
        "t_recency": round(t_recency, 1),
        "r_compliance": round(r_compliance, 1),
        "rpo_gap_hours": round(rpo_gap_hours, 1),
        "target_rpo_hours": target_rpo_hours,
        "backup_freshness_hours": round(backup_freshness_hours, 1),
        "last_test_days_ago": round(last_test_days_ago, 1),
        "rto_target_hours": rto_target_hours,
        "rto_actual_hours": rto_actual_hours,
        "primary_weakness": primary_weakness,
        "weaknesses": weaknesses
    }
