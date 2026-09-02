import pytest
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
