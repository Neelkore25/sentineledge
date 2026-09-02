import pytest
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
