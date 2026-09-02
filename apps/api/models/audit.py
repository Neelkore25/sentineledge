from sqlalchemy import Column, String, DateTime, JSON, Text
from datetime import datetime, timezone
from apps.api.core.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    actor = Column(String, nullable=False)
    role = Column(String, default="Analyst")
    action = Column(String, nullable=False)
    resource = Column(String, nullable=False)
    before_state = Column(JSON, nullable=True)
    after_state = Column(JSON, nullable=True)
    reason = Column(Text, nullable=False)
