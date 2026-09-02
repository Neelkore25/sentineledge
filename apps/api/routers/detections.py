from fastapi import APIRouter, Depends, HTTPException, Body
from apps.api.engine.rules import DEFAULT_RULES, SEVERITY_SCORES

router = APIRouter(prefix="/detections", tags=["detections"])

@router.get("/rules")
def get_rules():
    return [
        {
            "rule_id": r.rule_id,
            "name": r.name,
            "description": r.description,
            "severity": r.severity,
            "r_rule": SEVERITY_SCORES.get(r.severity, 50.0),
            "attack_category": r.attack_category,
            "enabled": r.enabled,
            "threshold": getattr(r, "threshold", getattr(r, "byte_threshold", getattr(r, "endpoint_threshold", None)))
        } for r in DEFAULT_RULES
    ]

@router.patch("/rules/{rule_id}")
def toggle_rule(rule_id: str, payload: dict = Body(...)):
    for r in DEFAULT_RULES:
        if r.rule_id == rule_id:
            if "enabled" in payload:
                r.enabled = bool(payload["enabled"])
            return {
                "rule_id": r.rule_id,
                "name": r.name,
                "enabled": r.enabled,
                "message": f"Rule {r.rule_id} status updated."
            }
    raise HTTPException(status_code=404, detail=f"Rule {rule_id} not found.")
