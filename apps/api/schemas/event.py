from pydantic import BaseModel, Field, ConfigDict, model_validator
from datetime import datetime
from typing import Optional, Any

class SecurityEventBase(BaseModel):
    source: str = "network_telemetry"
    user_id: Optional[str] = None
    asset_id: Optional[str] = None
    source_ip: Optional[str] = None
    event_type: str = "SECURITY_EVENT"
    action: Optional[str] = None
    status: str = "SUCCESS"
    endpoint: Optional[str] = None
    device_id: Optional[str] = None
    location: Optional[str] = None
    bytes_transferred: int = 0
    event_metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="before")
    @classmethod
    def normalize_input(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        d = dict(data)
        
        # 1. ID resolution
        if not d.get("id") and d.get("log_id"):
            d["id"] = str(d["log_id"])
            
        # 2. Source resolution
        if not d.get("source"):
            d["source"] = d.get("protocol") or d.get("source_ip") or "network_telemetry"
            
        # 3. Bytes calculation
        if not d.get("bytes_transferred") or d.get("bytes_transferred") == 0:
            b_sent = int(d.get("bytes_sent") or 0)
            b_recv = int(d.get("bytes_received") or 0)
            if b_sent or b_recv:
                d["bytes_transferred"] = b_sent + b_recv
                
        # 4. Status normalization
        st = str(d.get("status", "SUCCESS")).upper()
        if st in ("FAILED", "FAIL", "ERROR", "0"):
            d["status"] = "FAILURE"
        elif st in ("SUCCESS", "SUCCEEDED", "OK", "1"):
            d["status"] = "SUCCESS"
        else:
            d["status"] = st
            
        # 5. Endpoint resolution
        if not d.get("endpoint"):
            dst_ip = d.get("destination_ip")
            dst_port = d.get("destination_port")
            if dst_ip and dst_port:
                d["endpoint"] = f"{dst_ip}:{dst_port}"
            elif dst_ip:
                d["endpoint"] = str(dst_ip)
                
        # 6. Action resolution
        if not d.get("action"):
            d["action"] = str(d.get("event_type", "EVENT")).upper()
            
        # 7. Asset ID default
        if not d.get("asset_id"):
            d["asset_id"] = "ASSET_CUSTOMER_DB"
            
        # 8. Extra fields preserved in event_metadata
        known = {
            "id", "timestamp", "source", "user_id", "asset_id", "source_ip",
            "event_type", "action", "status", "endpoint", "device_id", "location",
            "bytes_transferred", "event_metadata"
        }
        meta = d.get("event_metadata") or {}
        if not isinstance(meta, dict):
            meta = {}
        for k, v in d.items():
            if k not in known and k not in meta:
                meta[k] = v
        d["event_metadata"] = meta
        return d

class SecurityEventCreate(SecurityEventBase):
    id: Optional[str] = None
    timestamp: Optional[datetime] = None

class SecurityEventResponse(SecurityEventBase):
    id: str
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)

