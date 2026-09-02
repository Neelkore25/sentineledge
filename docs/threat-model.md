# STRIDE Threat Model & Security Controls

| STRIDE Category | Potential Vulnerability | SentinelEdge Mitigations & Security Controls |
| :--- | :--- | :--- |
| **Spoofing** | Forged telemetry ingestion | Strict input validation via Pydantic; API keys for external forwarders. |
| **Tampering** | Modification of audit trail | Read-only ledger model; immutable event sequence logging in SQLite. |
| **Repudiation** | Denied incident response actions | Mandatory actor identity, role attribution, and human-in-the-loop audit logs. |
| **Information Disclosure** | Leakage of sensitive PII in AI prompts | AI service receives aggregated baseline deviations rather than raw passwords or unmasked credentials. |
| **Denial of Service** | Telemetry ingestion flood | Configurable pagination, batch limits, and sliding window boundaries. |
| **Elevation of Privilege** | Unauthorized role escalations | Role-based permissions (Analyst, Manager, Viewer) enforcing action confirmation boundaries. |
