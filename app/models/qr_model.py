from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    DateTime,
    Integer,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.configs.db import Base
import uuid

class QRCode(Base):
    __tablename__ = "qr_codes"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False, index=True)
    url = Column(String, nullable=False)
    color = Column(String(50), default="#000000", nullable=True)
    size = Column(Integer, default=200, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user_uuid = Column(UUID(as_uuid=True), ForeignKey("users.uuid"), nullable=False)
    user = relationship("User", back_populates="qr_codes")
    scans = relationship("Scan", back_populates="qr_code")