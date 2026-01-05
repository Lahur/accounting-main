from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional


class OutgoingRecipientBase(BaseModel):
    name: str
    address: str
    postal_code: str
    city: str
    oib: str


class OutgoingRecipientCreate(OutgoingRecipientBase):
    pass


class OutgoingRecipientUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    postal_code: Optional[str] = None
    city: Optional[str] = None
    oib: Optional[str] = None


class OutgoingRecipient(OutgoingRecipientBase):
    id: UUID
    modified: datetime

    class Config:
        from_attributes = True