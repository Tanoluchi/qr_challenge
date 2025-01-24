from uuid import UUID

from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional
from datetime import datetime


class CreateQRCodeSchema(BaseModel):
    url: HttpUrl
    color: Optional[str] = Field("black")  # Default color is black
    size: Optional[int] = Field(300)  # Default size is 300x300

    @property
    def url_str(self):
        return str(self.url)


class UpdateQRCodeSchema(BaseModel):
    color: Optional[str] = Field(None)
    size: Optional[int] = Field(None)
    url: Optional[HttpUrl] = Field(None)



class QRCodeSchema(BaseModel):
    uuid: UUID
    url: str
    color: str
    size: int
    created_at: datetime
    updated_at: datetime

class ListQRCodesSchema(BaseModel):
    qr_codes: List[QRCodeSchema]
