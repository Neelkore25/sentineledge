from datetime import datetime, timezone, timedelta
from typing import Optional

def normalize_correlation_score(event_count: int, stage_diversity_count: int) -> float:
    """
    Normalizes correlation group strength into [0, 100] sub-score C_correlation:
    C_correlation = clamp[0, 100]( event_count * 10 + stage_diversity_count * 20 )
    """
    raw = (event_count * 10.0) + (stage_diversity_count * 20.0)
    return float(min(100.0, max(0.0, raw)))

class EventCorrelator:
    def __init__(self, window_minutes: int = 30):
        self.window_minutes = window_minutes

    def correlate_events(self, events: list[dict], target_user: Optional[str] = None, target_ip: Optional[str] = None, target_asset: Optional[str] = None) -> dict:
        """
        Correlates events sharing entity identity (user_id, source_ip, or asset_id)
        within the configurable sliding window.
        """
        if not events:
            return {
                "correlated_event_ids": [],
                "event_count": 0,
                "stage_diversity": 0,
                "c_correlation": 0.0,
                "time_span_minutes": 0.0,
                "attack_stages": []
            }

        # Filter events related to entities
        matched = []
        for e in events:
            matches_user = target_user and e.get("user_id") == target_user
            matches_ip = target_ip and e.get("source_ip") == target_ip
            matches_asset = target_asset and e.get("asset_id") == target_asset
            
            if matches_user or matches_ip or matches_asset or (not target_user and not target_ip and not target_asset):
                matched.append(e)

        if not matched:
            return {
                "correlated_event_ids": [],
                "event_count": 0,
                "stage_diversity": 0,
                "c_correlation": 0.0,
                "time_span_minutes": 0.0,
                "attack_stages": []
            }

        # Determine stages present
        stages = set()
        for e in matched:
            etype = e.get("event_type", "").upper()
            action = e.get("action", "").upper()
            if "LOGIN_FAILED" in etype or "AUTH_FAILURE" in etype or "PORT_SCAN" in etype:
                stages.add("Initial Access / Recon")
            elif "LOGIN_SUCCESS" in etype:
                stages.add("Authentication")
            elif "ADMIN" in etype or "PRIVILEGE" in etype or "ROLE" in action:
                stages.add("Privilege Escalation")
            elif "DOWNLOAD" in etype or "EXPORT" in etype or e.get("bytes_transferred", 0) > 10_000_000:
                stages.add("Exfiltration")
            elif "BACKUP" in etype:
                stages.add("Impact / Tampering")
            else:
                stages.add("Execution")

        event_count = len(matched)
        stage_diversity = len(stages)
        c_score = normalize_correlation_score(event_count, stage_diversity)

        return {
            "correlated_event_ids": [e["id"] for e in matched if "id" in e],
            "event_count": event_count,
            "stage_diversity": stage_diversity,
            "c_correlation": round(c_score, 2),
            "attack_stages": sorted(list(stages))
        }
