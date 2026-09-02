from sqlalchemy import Column, String, Float, DateTime, JSON, Text
from datetime import datetime, timezone
from apps.api.core.database import Base

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String, index=True) # LOW, MEDIUM, HIGH, CRITICAL
    risk_score = Column(Float, default=0.0) # 0 - 100
    status = Column(String, default="OPEN", index=True) # OPEN, INVESTIGATING, MITIGATED, RESOLVED, FALSE_POSITIVE
    detected_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    first_seen = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_seen = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    affected_asset = Column(String, index=True, nullable=True)
    affected_user = Column(String, index=True, nullable=True)
    attack_category = Column(String, index=True)
    business_impact = Column(String, default="MEDIUM")
    confidence = Column(Float, default=0.85)
    correlation_group = Column(String, index=True)
    event_ids = Column(JSON, default=list)
    risk_breakdown = Column(JSON, default=dict)
    ai_summary = Column(Text, nullable=True)
    ai_hypothesis = Column(Text, nullable=True)
    ai_alternative = Column(Text, nullable=True)
    ai_missing_evidence = Column(Text, nullable=True)
    recommended_action = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
