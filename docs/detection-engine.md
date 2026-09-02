# Multi-Layer Detection Engine

## Layer 1: Configurable Deterministic Rules
- `RULE_AUTH_BRUTE_FORCE_001`: Threshold failed authentications within sliding window.
- `RULE_AUTH_SUSPICIOUS_GEO_002`: Successful authentication from unapproved geographic locations.
- `RULE_PRIV_ESCALATION_003`: Administrative permission mutations.
- `RULE_EXFIL_SPIKE_004`: Outbound transfers exceeding volume threshold.
- `RULE_BACKUP_CORRUPT_005`: Backup job failures and replica integrity errors.
- `RULE_RECON_PORT_SCAN_006`: Port and endpoint sweep probes.

## Layer 2: Robust Z-Score (MAD) Anomaly Engine
$$\text{MAD} = \text{median}\left(|x_i - \text{median}(x)|\right)$$
$$z_{\text{MAD}} = \frac{|x_{\text{observed}} - \text{median}(x)|}{1.4826 \times \text{MAD}}$$
$$S_{\text{behavior}} = \min\left(100.0, \max\left(0.0, \frac{z_{\text{MAD}}}{3.5} \times 100.0\right)\right)$$

## Layer 3: Temporal Event Correlation
Groups events occurring within $[t - \Delta t_{\text{window}}, t]$ (configurable, default: 30 minutes) sharing entity identity.
$$C_{\text{correlation}} = \min\left(100.0, \max\left(0.0, \text{event\_count} \times 10.0 + \text{stage\_diversity\_count} \times 20.0\right)\right)$$
