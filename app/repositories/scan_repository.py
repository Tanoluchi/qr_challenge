from typing import Any, Sequence

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import text, Row

from uuid import UUID

from app.configs.db import (
    get_db,
)
from app.models.scan_model import Scan


class ScanRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def get_all(self, qr_code_uuid: UUID) -> Sequence[Row[tuple[Any, ...] | Any]]:
        scan_logs_query = text("""
                SELECT 
                    uuid,
                    qr_uuid, 
                    ip, 
                    country, 
                    timezone,
                    created_at
                FROM scans
                WHERE (:qr_uuid IS NULL OR qr_uuid = :qr_uuid)
                ORDER BY created_at DESC
                LIMIT 1000
            """)
        return self.db.execute(
            scan_logs_query,
            {'qr_uuid': qr_code_uuid}
        ).fetchall()

    def create(self, scan: Scan) -> Scan:
        self.db_scan = scan
        self.db.add(self.db_scan)
        self.db.commit()
        self.db.refresh(self.db_scan)
        return self.db_scan

    def get(self, qr_code_uuid: UUID) -> Scan:
        return self.db.query(Scan).filter(Scan.uuid == qr_code_uuid).first()

    def get_total_scan(self, qr_code_uuid: UUID) -> Sequence[Row[tuple[Any, ...] | Any]]:
        total_scans_query = text("""
                SELECT 
                    qr_uuid, 
                    COUNT(*) as total_scans 
                FROM scans 
                WHERE (:qr_uuid IS NULL OR qr_uuid = :qr_uuid)
                GROUP BY qr_uuid
            """)
        return self.db.execute(
            total_scans_query,
            {'qr_uuid': qr_code_uuid}
        ).fetchall()
