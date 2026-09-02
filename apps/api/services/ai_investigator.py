import os
import json
from typing import Optional
import httpx
from apps.api.core.config import settings

class AIInvestigatorService:
    """
    Evidence-grounded AI investigator service.
    Strictly accepts only structured evidence packages (telemetry IDs, baseline metrics, asset context).
    Provides deterministic local fallback when no external API key is present.
    """

    @staticmethod
    def generate_deterministic_analysis(evidence_package: dict) -> dict:
        incident = evidence_package.get("incident", {})
        events = evidence_package.get("events", [])
        user_baseline = evidence_package.get("user_baseline", {})
        asset = evidence_package.get("asset", {})
        risk = evidence_package.get("risk_breakdown", {})
        recovery = evidence_package.get("recovery_context", {})

        event_ids = [e.get("id") for e in events if e.get("id")]
        event_types = list(set(e.get("event_type") for e in events if e.get("event_type")))
        unique_ips = list(set(e.get("source_ip") for e in events if e.get("source_ip")))
        username = incident.get("affected_user") or "unknown_user"
        asset_name = incident.get("affected_asset") or (asset.get("asset_name") if asset else "Critical Infrastructure")

        evidence_citations = []
        if any("LOGIN_FAILED" in str(et) for et in event_types):
            failed_evs = [e["id"] for e in events if "LOGIN_FAILED" in str(e.get("event_type", ""))]
            evidence_citations.append(f"Repeated authentication failures observed across event IDs: {', '.join(failed_evs[:4])}.")
        if any("LOGIN_SUCCESS" in str(et) for et in event_types):
            succ_evs = [e["id"] for e in events if "LOGIN_SUCCESS" in str(e.get("event_type", ""))]
            evidence_citations.append(f"Successful session authentication established in event ID: {', '.join(succ_evs)}.")
        if any("PRIVILEGE" in str(et) or "ADMIN" in str(et) for et in event_types):
            priv_evs = [e["id"] for e in events if "PRIVILEGE" in str(e.get("event_type", "")) or "ADMIN" in str(e.get("event_type", ""))]
            evidence_citations.append(f"Privilege modification or administrative elevation detected in: {', '.join(priv_evs)}.")
        if any("DOWNLOAD" in str(e.get("event_type", "")) or e.get("bytes_transferred", 0) > 50_000_000 for e in events):
            exfil_evs = [e["id"] for e in events if e.get("bytes_transferred", 0) > 50_000_000 or "DOWNLOAD" in str(e.get("event_type", ""))]
            evidence_citations.append(f"Anomalous high-volume outbound data transfer detected in: {', '.join(exfil_evs)}.")

        if not evidence_citations:
            evidence_citations = [f"Correlated {len(events)} telemetry events referencing IDs: {', '.join(event_ids[:5])}."]

        primary_hypothesis = f"Correlated activity indicates anomalous unauthorized access pattern targeting '{asset_name}' utilizing identity '{username}' from external source IP(s) {unique_ips}."
        alternative_explanation = f"Legitimate administrative operation conducted outside standard working hours via VPN or authorized external consultant."
        missing_evidence = f"Endpoint EDR process trees and multi-factor authentication challenge audit logs from identity provider are required to confirm host execution."
        
        recommended_actions = [
            f"Simulate session revocation and temporary credential lock for user '{username}'.",
            f"Inspect firewall logs for persistent egress connections to IP(s) {unique_ips}.",
            f"Verify backup immutability on asset '{asset_name}' (Current RPO Gap: {recovery.get('rpo_gap_hours', 0.0)}h)."
        ]

        summary = f"Automated evidence correlation assembled {len(events)} security events against {asset_name}. Risk model scored technical and business impact at {risk.get('composite_risk_score', incident.get('risk_score', 75.0))}/100 ({risk.get('severity_band', 'HIGH')})."

        return {
            "mode": "Local Research Assistant (Deterministic Evidence Grounded)",
            "summary": summary,
            "primary_hypothesis": primary_hypothesis,
            "alternative_explanation": alternative_explanation,
            "evidence_citations": evidence_citations,
            "missing_evidence": missing_evidence,
            "confidence_score": 0.88,
            "recommended_actions": recommended_actions,
            "model_used": "SentinelEdge-Deterministic-Engine-v1"
        }

    @classmethod
    async def investigate_incident(cls, evidence_package: dict) -> dict:
        provider = settings.AI_PROVIDER.lower()
        api_key = settings.AI_API_KEY

        if provider in ("openai", "gemini", "anthropic") and api_key:
            try:
                system_prompt = (
                    "You are the SentinelEdge Incident Investigation Assistant. "
                    "You MUST use ONLY the supplied evidence package. "
                    "NEVER invent events, users, IP addresses, timestamps, or system actions. "
                    "Explicitly cite supplied event IDs. "
                    "Separate observed facts from hypotheses. "
                    "Return valid JSON matching the requested schema."
                )
                user_content = json.dumps(evidence_package)

                if provider == "openai":
                    async with httpx.AsyncClient(timeout=15.0) as client:
                        prompt_msg = "Investigate this evidence package and return JSON with summary, primary_hypothesis, alternative_explanation, evidence_citations (list), missing_evidence, confidence_score (float 0-1), recommended_actions (list): " + user_content
                        resp = await client.post(
                            "https://api.openai.com/v1/chat/completions",
                            headers={"Authorization": f"Bearer {api_key}"},
                            json={
                                "model": settings.AI_MODEL or "gpt-4o-mini",
                                "messages": [
                                    {"role": "system", "content": system_prompt},
                                    {"role": "user", "content": prompt_msg}
                                ],
                                "response_format": {"type": "json_object"}
                            }
                        )
                        if resp.status_code == 200:
                            data = resp.json()
                            content = data["choices"][0]["message"]["content"]
                            parsed = json.loads(content)
                            parsed["mode"] = f"Cloud AI Provider ({provider})"
                            parsed["model_used"] = settings.AI_MODEL
                            return parsed
            except Exception as e:
                print(f"External AI Provider error: {e}. Falling back to deterministic analysis.")

        return cls.generate_deterministic_analysis(evidence_package)
