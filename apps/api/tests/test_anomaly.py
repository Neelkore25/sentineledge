import pytest
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
