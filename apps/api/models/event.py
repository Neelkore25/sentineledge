from sqlalchemy import Column, String, DateTime, JSON, BigInteger
from datetime import datetime, timezone
from apps.api.core.database import Base

class SecurityEvent(Base):
    __tablename__ = "security_events"

    id = Column(String, primary_key=True, index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    source = Column(String, index=True)
    user_id = Column(String, index=True, nullable=True)
    asset_id = Column(String, index=True, nullable=True)
    source_ip = Column(String, index=True, nullable=True)
    event_type = Column(String, index=True)
    action = Column(String, nullable=True)
    status = Column(String, index=True)
    endpoint = Column(String, nullable=True)
    device_id = Column(String, nullable=True)
    location = Column(String, nullable=True)
    bytes_transferred = Column(BigInteger, default=0)
    event_metadata = Column(JSON, default=dict)
