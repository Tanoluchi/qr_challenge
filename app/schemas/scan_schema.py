from uuid import UUID

from pydantic import BaseModel
from typing import List
from datetime import datetime

class ScanStatisticsSchema(BaseModel):
    uuid: UUID
    qr_uuid: UUID
    ip: str | None = None
    country: str | None = None
    timezone: str | None = None
    created_at: datetime

class ScanCounterSchema(BaseModel):
    qr_uuid: UUID
    scans: int

class QRCodeStatisticsSchema(BaseModel):
    total_scans: List[ScanCounterSchema]
    scan_logs: List[ScanStatisticsSchema]