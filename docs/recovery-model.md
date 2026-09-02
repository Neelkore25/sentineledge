# Recovery Readiness Model & The Recovery Window

$$\text{Readiness Index} = 0.35 B_{\text{freshness}} + 0.25 V_{\text{verified}} + 0.20 T_{\text{test\_recency}} + 0.20 R_{\text{rto\_rpo\_compliance}}$$

## Key Metrics
- **Backup Freshness ($B_{\text{freshness}}$)**: Evaluates elapsed time since last snapshot against Target RPO.
- **Verification Status ($V_{\text{verified}}$)**: 100% if cryptographic checksum verified, 0% if unverified.
- **Drill Recency ($T_{\text{test\_recency}}$)**: Decays after 30 days; flagged overdue after 60 days.
- **SLA Compliance ($R_{\text{compliance}}$)**: Restorability ratio comparing actual drill duration against SLA target.
