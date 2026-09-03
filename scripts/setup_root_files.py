import os

def write_file(path, content):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

# 1. README.md
write_file("README.md", """# SentinelEdge

> **Detect clearly. Respond deliberately. Recover ready.**  
> *An Explainable AI-Assisted Cybersecurity and Recovery Readiness Platform for SMEs*

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI%200.110-009688.svg)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Frontend-Next.js%2014-black.svg)](https://nextjs.org)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB.svg)](https://python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6-blue.svg)](https://www.typescriptlang.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 1. Problem Statement

Small-to-Medium Enterprises (SMEs) face a critical cybersecurity dilemma: traditional enterprise SIEM/SOC platforms are prohibitively expensive and generate overwhelming alert fatigue, while small IT teams lack dedicated security analysts. Most critically, conventional tools operate in a vacuum—detecting technical alerts without assessing business asset impact or verifying whether the organization is prepared to recover if an attack succeeds. **SentinelEdge** bridges this gap by unifying multi-layer threat detection, explainable risk scoring, business impact quantification, evidence-grounded AI investigation, and real-time disaster recovery posture into a single lightweight platform.

---

## 2. Architecture

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

---

## 3. Research Framing & Hypotheses

- **Core Research Question**: *Can a lightweight, explainable AI-assisted cybersecurity platform improve incident prioritization and recovery readiness for resource-constrained SMEs compared with conventional rule-based detection?*
- **Hypothesis 1 (Hybrid Detection)**: Multi-layer detection combining deterministic rules, statistical Robust Z-Score (MAD) behavioral baselines, and temporal event correlation reduces false-positive alert fatigue while preserving high detection recall.
- **Hypothesis 2 (Evidence Grounding)**: Restricting AI investigation to strictly supplied telemetry IDs, baseline deviations, and explicit uncertainty boundaries significantly enhances analyst comprehension without hallucinations.
- **Hypothesis 3 (Coupled Recovery Readiness)**: Coupling technical threat severity with organizational asset criticality, downtime exposure, and backup RPO/RTO readiness produces actionable remediation decisions.

*See [`docs/research.md`](docs/research.md) and [`docs/evaluation.md`](docs/evaluation.md) for complete academic documentation.*

---

## 4. Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | Next.js 14 (App Router), React 18, TypeScript, Tailwind CSS ("Security Editorial" design system), Framer Motion, Recharts, Lucide Icons |
| **Backend** | FastAPI (Python 3.12), Pydantic v2, SQLAlchemy, SQLite |
| **Detection & Analytics** | Python 3-Layer Detection Engine, Robust Z-Score (MAD) Anomaly Detector, Sliding-Window Temporal Correlator |
| **AI Intelligence** | Multi-provider AI Investigator (OpenAI / Gemini / Anthropic) + Deterministic Local Research Assistant Fallback |
| **Testing & Quality** | Pytest, Pytest-Asyncio, TypeScript Strict Typing, ESLint |

---

## 5. UI Showcase & Signature Components

- **Operations Dashboard**: Dual-mode (Analyst vs Executive), Organization Risk gauge, Incident Pressure distribution, live event stream.
- **Incident Evidence Rail**: Visual lifecycle tracker (`Observed → Correlated → Scored → Explained → Prioritized → Responded`).
- **Risk Breakdown Stack**: Horizontal evidence stack decomposing the composite score into 5 individually normalized sub-scores ($R_{\\text{rule}}, S_{\\text{behavior}}, C_{\\text{correlation}}, A_{\\text{criticality}}, B_{\\text{impact}}$).
- **The Recovery Window**: Compares Target RPO vs Current Snapshot Gap, Last Verified Test recency, and disaster recovery SLA readiness.
- **Simulation Lab**: 7 interactive, zero-risk attack scenarios ("Too Many Doors", "Unexpected Visitor", "The Privilege Jump", "The Large Download", "The Long Night", "Recon in the Dark", "Backup Severed").

---

## 6. Quickstart Guide

### Prerequisites
- Python 3.12+
- Node.js 18+ and npm

### 1. Clone & Setup Environment
```bash
git clone https://github.com/your-username/sentineledge.git
cd sentineledge
cp .env.example .env
```

### 2. Run Backend (FastAPI)
```bash
cd apps/api
pip install -r requirements.txt
python -m pytest tests -v     # Run test suite
python main.py                # Runs on http://localhost:8000
```

### 3. Run Frontend (Next.js)
```bash
cd apps/web
npm install
npm run dev                  # Runs on http://localhost:3000
```

Open [`http://localhost:3000`](http://localhost:3000) in your browser.

---

## 7. REST API Documentation Summary

The FastAPI backend provides interactive Swagger UI docs at [`http://localhost:8000/docs`](http://localhost:8000/docs).

| Route | Method | Description |
| :--- | :--- | :--- |
| `/api/v1/telemetry` | `GET`, `POST` | Query, filter, paginate, and ingest security telemetry events |
| `/api/v1/incidents` | `GET` | List and search correlated security incidents |
| `/api/v1/incidents/{id}` | `GET`, `PATCH` | Retrieve incident details with correlated events or update status |
| `/api/v1/incidents/{id}/respond` | `POST` | Execute human-in-the-loop response action with audit logging |
| `/api/v1/simulation/scenarios` | `GET` | Retrieve list of 7 interactive attack scenarios |
| `/api/v1/simulation/run` | `POST` | Inject scenario telemetry and trigger live detection & correlation |
| `/api/v1/detections/rules` | `GET`, `PATCH` | List active detection rules and toggle enablement/thresholds |
| `/api/v1/behavior/users` | `GET` | Retrieve user behavioral baselines and Robust Z-Score MAD metrics |
| `/api/v1/recovery/inventory` | `GET` | Retrieve backup inventory, verification status, and readiness score |
| `/api/v1/ai/investigate` | `POST` | Trigger evidence-grounded AI consultation with citation badges |
| `/api/v1/audit` | `GET` | Retrieve immutable audit ledger entries |
| `/api/v1/settings` | `GET`, `PUT` | Read/update settings (including `correlation_window_minutes`) |
| `/api/v1/stats/overview` | `GET` | Aggregate stats for top status strip, risk trend, and pressure |

---

## 8. Application Routes

| Route | Page | Purpose |
| :--- | :--- | :--- |
| `/` | Landing / Research Portal | Public overview, live preview, 3 pillars, interactive workflow, limitations |
| `/demo` | Guided Demo Launcher | Role selector (Analyst Demo, Executive Demo, Viewer Demo) |
| `/dashboard` | Operations Center | Dual-mode Analyst/Executive view, Organization Risk, Incident Pressure |
| `/incidents` | Incident Registry | High-density sortable/filterable table with severity badges |
| `/incidents/[id]` | Investigation Canvas | Evidence Rail, Risk Breakdown Stack, AI panel, Response drawer |
| `/events` | Telemetry Explorer | Raw event logs with IP/user/type filters and JSON payload viewer |
| `/attack-stories` | Attack Storyboards | Vertical progressive timeline diagrams visualizing multi-stage attacks |
| `/simulation` | Simulation Lab | 7 human-named scenarios for safe real-time telemetry generation |
| `/detections` | Detection Rules | Active rules list, severity mappings, and threshold controls |
| `/behavior` | Behavioral Baselines | User baseline profiles and MAD deviation calculations |
| `/recovery` | Recovery Readiness | Backup inventory, snapshot verification, and RTO/RPO SLA compliance |
| `/ai-investigator` | AI Consultation Studio | Evidence-grounded consultation with strict citation verification |
| `/reports` | Reports Center | Post-mortem reviews and printable/exportable PDF summaries |
| `/audit` | Audit Log | Immutable ledger of all human-in-the-loop response actions |
| `/research` | Research Hub | Academic hypotheses, methodology, and benchmark evaluation |
| `/settings` | System Settings | Configurable correlation window, detection thresholds, and AI provider |

---

## 9. Live Demo

- **Web Application**: *[Deployed on Render / Vercel — Placeholder]*
- **API Backend**: *[Deployed on Render — Placeholder]*

---

## 10. Limitations & Disclaimers

> [!NOTE]
> SentinelEdge is a production-quality research prototype built for evaluation and demonstration. All telemetry streams are synthesized safely. AI investigator outputs are advisory recommendations designed for human-in-the-loop validation.

---

## 11. Contributing & Security

- Contributions are welcome! Please review [`CONTRIBUTING.md`](CONTRIBUTING.md) for development workflows.
- For vulnerability reports, please consult [`SECURITY.md`](SECURITY.md).

---

## 12. License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for details.
""")

# 2. CONTRIBUTING.md
write_file("CONTRIBUTING.md", """# Contributing to SentinelEdge

Thank you for contributing to SentinelEdge!

## Development Setup
1. **Backend**:
   ```bash
   cd apps/api
   pip install -r requirements.txt
   python -m pytest tests -v
   python main.py
   ```
2. **Frontend**:
   ```bash
   cd apps/web
   npm install
   npm run dev
   ```

## Branch Naming Convention
- `feature/<name>` — New capabilities or components
- `fix/<name>` — Bug fixes and engine adjustments
- `docs/<name>` — Research and documentation updates

## Pull Request Guidelines
- Ensure all backend unit and API tests pass: `pytest apps/api/tests`
- Ensure frontend passes typechecking: `npm run typecheck`
- Keep commits atomic and clearly described.
""")

# 3. SECURITY.md
write_file("SECURITY.md", """# Security Policy

## Reporting Vulnerabilities
SentinelEdge is a research prototype. If you discover a potential security issue or vulnerability, please responsibly disclose it by emailing:
`security-research@sentineledge.internal` (or open a confidential GitHub Security Advisory).

Please provide:
- Description of the vulnerability
- Steps to reproduce
- Potential impact assessment

We appreciate responsible disclosure.
""")

# 4. LICENSE (MIT)
write_file("LICENSE", """MIT License

Copyright (c) 2026 SentinelEdge Project Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""")

# 5. .env.example
write_file(".env.example", """# SentinelEdge Environment Variables

# Backend Database (SQLite default for zero-config local runs; PostgreSQL compatible)
DATABASE_URL=sqlite:///./sentineledge.db

# Detection Engine Settings
CORRELATION_WINDOW_MINUTES=30
BRUTE_FORCE_THRESHOLD=5
DATA_EXFIL_THRESHOLD_MB=500

# AI Provider Configuration ('local' | 'openai' | 'gemini' | 'anthropic')
AI_PROVIDER=local
AI_API_KEY=
AI_MODEL=gpt-4o-mini

# Frontend API Endpoint
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
""")

# 6. .gitignore
write_file(".gitignore", """# Dependencies
node_modules/
.pnp
.pnp.js

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv/
.pytest_cache/

# Databases
*.db
*.sqlite
*.sqlite3

# Next.js Build
.next/
out/
build/
dist/

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Environment & Secrets
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# OS
.DS_Store
Thumbs.db
""")

print("README, CONTRIBUTING, SECURITY, LICENSE, .env.example, .gitignore created!")
