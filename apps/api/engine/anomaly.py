import numpy as np
from typing import Sequence, Optional

def calculate_mad(values: Sequence[float]) -> tuple[float, float]:
    """
    Calculates Median and Median Absolute Deviation (MAD).
    Returns (median, MAD).
    """
    arr = np.array(values, dtype=float)
    if len(arr) == 0:
        return 0.0, 1.0
    median = float(np.median(arr))
    deviations = np.abs(arr - median)
    mad = float(np.median(deviations))
    if mad == 0.0:
        # Fallback to mean absolute deviation or epsilon to prevent division by zero
        mad = float(np.mean(deviations)) or 1.0
    return median, mad

def robust_z_score(observed_value: float, baseline_values: Sequence[float]) -> float:
    """
    Calculates Modified Robust Z-score:
    z_MAD = |x - median| / (1.4826 * MAD)
    """
    median, mad = calculate_mad(baseline_values)
    denominator = 1.4826 * mad
    if denominator == 0.0:
        return 0.0
    return float(abs(observed_value - median) / denominator)

def normalize_behavior_score(z_mad: float, sensitivity_multiplier: float = 3.5) -> float:
    """
    Normalizes Robust Z-Score into [0, 100] sub-score S_behavior.
    S_behavior = clamp[0, 100]( (z_mad / 3.5) * 100 )
    """
    normalized = (z_mad / sensitivity_multiplier) * 100.0
    return float(min(100.0, max(0.0, normalized)))

def evaluate_user_behavior(
    observed_download_mb: float,
    observed_login_hour: int,
    user_baseline: dict
) -> dict:
    """
    Evaluates behavioral deviation across download volume and login hour.
    Returns composite normalized S_behavior sub-score in [0, 100] and detailed features.
    """
    history = user_baseline.get("download_history_json", [40.0, 42.0, 45.0, 48.0, 44.0, 46.0, 43.0])
    z_download = robust_z_score(observed_download_mb, history)
    s_download = normalize_behavior_score(z_download)
    
    # Login hour deviation check
    start_hour = user_baseline.get("typical_login_start_hour", 9)
    end_hour = user_baseline.get("typical_login_end_hour", 18)
    
    if start_hour <= observed_login_hour <= end_hour:
        hour_penalty = 0.0
    else:
        # Distance outside working window in hours
        dist = min(abs(observed_login_hour - start_hour), abs(observed_login_hour - end_hour))
        hour_penalty = min(100.0, dist * 15.0)
    
    # Composite behavioral deviation
    s_behavior = min(100.0, max(0.0, 0.7 * s_download + 0.3 * hour_penalty))
    
    return {
        "s_behavior": round(s_behavior, 2),
        "z_mad_download": round(z_download, 2),
        "s_download_deviation": round(s_download, 2),
        "observed_download_mb": observed_download_mb,
        "baseline_median_download_mb": round(float(np.median(history)), 1),
        "hour_deviation_penalty": round(hour_penalty, 2),
        "observed_login_hour": observed_login_hour,
        "expected_hour_range": f"{start_hour:02d}:00 - {end_hour:02d}:00"
    }
