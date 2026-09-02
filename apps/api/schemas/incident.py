from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, Any

class RiskBreakdownSchema(BaseModel):
    r_rule: float = Field(description="Normalized Rule Severity Sub-score [0, 100]")
    s_behavior: float = Field(description="Normalized Behavioral Deviation Sub-score [0, 100]")
    c_correlation: float = Field(description="Normalized Correlation Group Sub-score [0, 100]")
    a_criticality: float = Field(description="Normalized Asset Criticality Sub-score [0, 100]")
    b_impact: float = Field(description="Normalized Business Impact Sub-score [0, 100]")
    weights: dict[str, float] = Field(description="Weights applied to each sub-score")
    weighted_contributions: dict[str, float] = Field(description="Weighted points contributed")
    composite_risk_score: float = Field(description="Total composite risk score [0, 100]")
    severity_band: str = Field(description="LOW, MEDIUM, HIGH, CRITICAL")
    formula: str = Field(description="Human-readable formula string")

class IncidentBase(BaseModel):
    title: str
    description: str
    severity: str
    risk_score: float
    status: str = "OPEN"
    affected_asset: Optional[str] = None
    affected_user: Optional[str] = None
    attack_category: str
    business_impact: str = "MEDIUM"
    confidence: float = 0.85
    correlation_group: str
    event_ids: list[str] = Field(default_factory=list)
    risk_breakdown: Optional[dict[str, Any]] = Field(default_factory=dict)
    ai_summary: Optional[str] = None
    ai_hypothesis: Optional[str] = None
    ai_alternative: Optional[str] = None
    ai_missing_evidence: Optional[str] = None
    recommended_action: Optional[str] = None

class IncidentCreate(IncidentBase):
    id: Optional[str] = None
    detected_at: Optional[datetime] = None
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None

class IncidentResponse(IncidentBase):
    id: str
    detected_at: datetime
    first_seen: datetime
    last_seen: datetime
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
