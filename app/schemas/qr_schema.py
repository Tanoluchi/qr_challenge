from uuid import UUID

from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional
from datetime import datetime


class CreateQRCodeSchema(BaseModel):
    url: HttpUrl = Field(examples=['https://google.com/'])
    color: Optional[str] = Field("black", description="The color must be in hexadecimal", examples=['#0000FF'])  # Default color is black
    size: Optional[int] = Field(300, description="The size must be integer", examples=['400'])  # Default size is 300x300

    @property
    def url_str(self):
        return str(self.url)


class UpdateQRCodeSchema(BaseModel):
    color: Optional[str] = Field(None, description="The field is optional and must be color in hexadecimal", examples=['#0000FF'])
    size: Optional[int] = Field(None, description="The field is optional")
    url: Optional[HttpUrl] = Field(None, description="The field is optional")


class QRCodeSchema(BaseModel):
    uuid: UUID
    url: str
    color: str
    size: int
    created_at: datetime
    updated_at: datetime

class ListQRCodesSchema(BaseModel):
    qr_codes: List[QRCodeSchema]
