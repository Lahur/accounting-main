from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from decimal import Decimal
from typing import Optional


class OutgoingBillBase(BaseModel):
    project_name: str
    project_description: str
    base_price: Decimal
    pdv_price: Decimal
    price: Decimal
    price_text: str
    date_time: datetime
    recipient_id: UUID
    bill_number: int


class OutgoingBillCreate(OutgoingBillBase):
    pass


class OutgoingBillUpdate(BaseModel):
    project_name: Optional[str] = None
    project_description: Optional[str] = None
    base_price: Optional[Decimal] = None
    pdv_price: Optional[Decimal] = None
    price: Optional[Decimal] = None
    price_text: Optional[str] = None
    date_time: Optional[datetime] = None
    recipient_id: Optional[UUID] = None
    bill_number: Optional[int] = None


class OutgoingBill(OutgoingBillBase):
    id: UUID
    modified: datetime

    class Config:
        from_attributes = True