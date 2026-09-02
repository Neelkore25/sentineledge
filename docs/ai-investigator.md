# Evidence-Grounded AI Investigator Specification

## Strict Grounding Contract
1. Never invent logs, users, IP addresses, timestamps, or system endpoints.
2. Every claim in the Primary Hypothesis must cite one or more supplied Event IDs (`EV-1042`).
3. Must clearly distinguish observed telemetry facts from analytical hypotheses.
4. Must declare confidence score and explicitly state missing evidence required for confirmation.
5. Operates in deterministic offline mode when no external API key is configured.
