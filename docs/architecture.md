# SentinelEdge System Architecture

SentinelEdge is designed specifically for resource-constrained Small-to-Medium Enterprises (SMEs) requiring high explainability, minimal false positives, and tight coupling with disaster recovery readiness.

## Core Architectural Flow
```text
+-----------------------+     +--------------------------+     +----------------------------+
|  Security Telemetry   | --> | Normalization & Ingest   | --> | 3-Layer Detection Engine   |
| (Auth, Egress, Cloud) |     | (Canonical Event Schema) |     | (Rules + Robust MAD + Corr)|
+-----------------------+     +--------------------------+     +----------------------------+
                                                                             |
                                                                             v
+-----------------------+     +--------------------------+     +----------------------------+
| Business Impact Model | <-- | Explainable Risk Model   | <-- | Normalized Sub-Scores      |
| (Downtime, Blast Rad) |     | (Research Risk Model v1) |     | (R_rule, S_beh, C_corr...) |
+-----------------------+     +--------------------------+     +----------------------------+
            |
            v
+-----------------------+     +--------------------------+     +----------------------------+
| Recovery Window Posture| --> | Evidence-Grounded AI     | --> | Human-in-the-Loop Response |
| (RPO/RTO SLAs, Tests) |     | (Citations, Hypotheses)  |     | & Tamper-Evident Audit Log |
+-----------------------+     +--------------------------+     +----------------------------+
```

## Backend Services
- **FastAPI / Python 3.12 Engine**: Hosts all detection logic, statistical anomaly engines, correlation algorithms, and REST APIs.
- **SQLite Database**: Lightweight, zero-config relational store via SQLAlchemy.
- **AI Investigator Service**: Structured evidence assembler providing deterministic local fallback and optional external LLM integration.

## Frontend Client
- **Next.js 14 App Router**: Clean, responsive UI implementing the "Security Editorial" design system.
- **Dual-Mode Experience**: Instant toggle between granular Analyst View and strategic Executive View.
