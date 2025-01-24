from fastapi import Depends
from sqlalchemy.orm import Session

from uuid import UUID

from app.configs.db import (
    get_db,
)
from app.models.qr_model import QRCode
from app.schemas.qr_schema import UpdateQRCodeSchema


class QRCodeRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def get_all(self, user_uuid) -> list[QRCode]:
        return self.db.query(QRCode).filter(QRCode.user_uuid == user_uuid).all()

    def create(self, qr_code: QRCode) -> QRCode:
        self.db_qr_code = qr_code
        self.db.add(self.db_qr_code)
        self.db.commit()
        self.db.refresh(self.db_qr_code)
        return self.db_qr_code

    def get(self, qr_code_uuid: UUID) -> QRCode:
        return self.db.query(QRCode).filter(QRCode.uuid == qr_code_uuid).first()

    def update(self, qr_code: QRCode, qr_code_body: UpdateQRCodeSchema):
        update_data = qr_code_body.model_dump(exclude_unset=True)

        if 'url' in update_data and hasattr(update_data['url'], 'unicode_string'):
            update_data['url'] = str(update_data['url'])

        for key, value in update_data.items():
            setattr(qr_code, key, value)

        self.db.commit()
        self.db.refresh(qr_code)
        return qr_code
