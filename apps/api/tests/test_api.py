import pytest
from fastapi.testclient import TestClient
from apps.api.main import app
from apps.api.core.database import Base, engine, SessionLocal
from apps.api.seeder.seed_db import seed_database

@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    seed_database(db)
    db.close()
    with TestClient(app) as c:
        yield c

def test_root_and_health(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["platform"] == "SentinelEdge"

    r_h = client.get("/health")
    assert r_h.status_code == 200
    assert r_h.json()["status"] == "healthy"

def test_stats_overview(client):
    r = client.get("/api/v1/stats/overview")
    assert r.status_code == 200
    data = r.json()
    assert "organization_risk_score" in data
    assert "recovery_readiness_score" in data
    assert "incident_pressure" in data
    assert "open_incidents_count" in data

def test_telemetry_endpoints(client):
    # GET telemetry
    r = client.get("/api/v1/telemetry?limit=10")
    assert r.status_code == 200
    data = r.json()
    assert "items" in data
    assert "total" in data

    # POST ingest event
    new_event = {
        "source": "vpn_gateway",
        "user_id": "finance_admin",
        "asset_id": "ASSET_AUTH_PORTAL",
        "source_ip": "10.0.9.99",
        "event_type": "LOGIN_SUCCESS",
        "action": "LOGIN",
        "status": "SUCCESS",
        "endpoint": "/auth/sso",
        "bytes_transferred": 1024,
        "event_metadata": {"mfa": True}
    }
    r_post = client.post("/api/v1/telemetry", json=new_event)
    assert r_post.status_code == 200
    assert r_post.json()["status"] == "ingested"

def test_incidents_lifecycle(client):
    # 1. List incidents
    r = client.get("/api/v1/incidents")
    assert r.status_code == 200
    incidents = r.json()
    assert len(incidents) > 0
    inc_id = incidents[0]["id"]

    # 2. Get incident by id
    r_get = client.get(f"/api/v1/incidents/{inc_id}")
    assert r_get.status_code == 200
    inc_data = r_get.json()
    assert "incident" in inc_data
    assert "related_events" in inc_data

    # 3. Update status
    r_patch = client.patch(f"/api/v1/incidents/{inc_id}/status", json={
        "status": "INVESTIGATING",
        "reason": "Analyst investigating suspicious activity."
    })
    assert r_patch.status_code == 200
    assert r_patch.json()["new_status"] == "INVESTIGATING"

    # 4. Human-approved response action
    r_resp = client.post(f"/api/v1/incidents/{inc_id}/respond", json={
        "action_type": "SIMULATE_ACCOUNT_LOCK",
        "target": "finance_admin",
        "reason": "Suspicious login burst confirmed."
    })
    assert r_resp.status_code == 200
    assert r_resp.json()["status"] == "executed"
    assert r_resp.json()["new_status"] == "MITIGATED"

def test_simulation_scenarios_and_run(client):
    # 1. Get scenarios
    r_scen = client.get("/api/v1/simulation/scenarios")
    assert r_scen.status_code == 200
    scenarios = r_scen.json()
    assert len(scenarios) >= 7

    # 2. Run scenario "brute_force" (Too Many Doors)
    r_run = client.post("/api/v1/simulation/run", json={"scenario_key": "brute_force"})
    assert r_run.status_code == 200
    res = r_run.json()
    assert res["status"] == "completed"
    assert "incident_id" in res
    assert "risk_score" in res
    assert "risk_breakdown" in res
    assert "ai_investigation" in res
    # Verify sub-scores are normalized in [0, 100]
    rb = res["risk_breakdown"]
    assert 0 <= rb["r_rule"] <= 100
    assert 0 <= rb["s_behavior"] <= 100
    assert 0 <= rb["c_correlation"] <= 100
    assert 0 <= rb["a_criticality"] <= 100
    assert 0 <= rb["b_impact"] <= 100

def test_detections_rules(client):
    r = client.get("/api/v1/detections/rules")
    assert r.status_code == 200
    rules = r.json()
    assert len(rules) >= 6

def test_behavior_baselines(client):
    r = client.get("/api/v1/behavior/users")
    assert r.status_code == 200
    users = r.json()
    assert len(users) >= 3
    assert "baseline_evaluation" in users[0]

def test_recovery_inventory(client):
    r = client.get("/api/v1/recovery/inventory")
    assert r.status_code == 200
    data = r.json()
    assert "overall_readiness_score" in data
    assert "items" in data

def test_ai_investigate(client):
    r_inc = client.get("/api/v1/incidents")
    inc_id = r_inc.json()[0]["id"]

    r_ai = client.post("/api/v1/ai/investigate", json={"incident_id": inc_id})
    assert r_ai.status_code == 200
    res = r_ai.json()
    assert "summary" in res
    assert "primary_hypothesis" in res
    assert "evidence_citations" in res
    assert "recommended_actions" in res

def test_audit_logs(client):
    r = client.get("/api/v1/audit?limit=20")
    assert r.status_code == 200
    logs = r.json()
    assert len(logs) > 0

def test_settings_configurable_correlation_window(client):
    # 1. Get settings
    r = client.get("/api/v1/settings")
    assert r.status_code == 200
    data = r.json()
    assert "correlation_window_minutes" in data

    # 2. Update correlation window from 30 to 45 minutes
    r_up = client.put("/api/v1/settings/correlation_window_minutes", json={"value": "45"})
    assert r_up.status_code == 200
    assert r_up.json()["value"] == "45"

    # 3. Verify updated setting
    r_get = client.get("/api/v1/settings")
    assert r_get.json()["correlation_window_minutes"]["value"] == "45"

    # Reset back to 30
    client.put("/api/v1/settings/correlation_window_minutes", json={"value": "30"})
