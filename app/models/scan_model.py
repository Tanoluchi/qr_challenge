from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    DateTime
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.configs.db import Base
import uuid

class Scan(Base):
    __tablename__ = "scans"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    qr_uuid = Column(UUID(as_uuid=True), ForeignKey("qr_codes.uuid"), nullable=False)
    ip = Column(String(45), nullable=True)
    country = Column(String(100), nullable=True)
    timezone = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship to QR codes
    qr_code = relationship("QRCode", back_populates="scans")