from fastapi import APIRouter, Query
from datetime import datetime
from typing import List, Optional, Union
from service.bill_service import BillService
from model import OutgoingRecipient, OutgoingBill, OutgoingRecipientCreate, OutgoingBillCreate

router = APIRouter(prefix="/bills", tags=["bills"])
bill_service = BillService()

@router.get("/recipients", response_model=List[OutgoingRecipient])
async def get_recipients(modified_after: Optional[datetime] = Query(None)):
    return bill_service.get_recipients_by_modified(modified_after)

@router.get("", response_model=List[OutgoingBill])
async def get_bills(modified_after: Optional[datetime] = Query(None)):
    return bill_service.get_bills_by_modified(modified_after)

@router.post("/recipients", response_model=List[OutgoingRecipient])
async def save_recipients(recipients: List[Union[OutgoingRecipient, OutgoingRecipientCreate]]):
    return bill_service.save_recipients(recipients)

@router.post("", response_model=List[OutgoingBill])
async def save_bills(bills: List[Union[OutgoingBill, OutgoingBillCreate]]):
    return bill_service.save_bills(bills)

