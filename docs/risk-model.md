# SentinelEdge Research Risk Model v1

All 5 sub-scores are explicitly normalized to $[0, 100]$ prior to applying linear weights ($\sum w_i = 1.0$):

$$\text{Risk Score} = \min\left(100.0, \max\left(0.0, 0.25 R_{\text{rule}} + 0.20 S_{\text{behavior}} + 0.20 C_{\text{correlation}} + 0.20 A_{\text{criticality}} + 0.15 B_{\text{impact}}\right)\right)$$

## Severity Bands
- `0–24`: **LOW**
- `25–49`: **MEDIUM**
- `50–74`: **HIGH**
- `75–100`: **CRITICAL**
