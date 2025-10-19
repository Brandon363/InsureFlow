from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional, List

from Model.ResponseModel import BaseResponse
from Utils.Enums import PaymentStatus, PaymentMethod, EntityStatus


class PaymentDTO(BaseModel):
    id: int
    user_id: int
    policy_id: int
    amount: float
    status: PaymentStatus
    payment_method: PaymentMethod
    transaction_id: str
    receipt_url: Optional[str] = None
    paid_at: date
    due_date: date
    date_created: datetime
    date_updated: Optional[datetime] = None
    entity_status: EntityStatus

    model_config = ConfigDict(from_attributes=True)


class PaymentCreate(BaseModel):
    user_id: int
    policy_id: int
    amount: float
    status: PaymentStatus
    payment_method: PaymentMethod
    transaction_id: str
    receipt_url: Optional[str] = None
    paid_at: date
    due_date: date


class PaymentUpdate(BaseModel):
    user_id: Optional[int] = None
    policy_id: Optional[int] = None
    amount: Optional[float] = None
    status: Optional[PaymentStatus] = None
    payment_method: Optional[PaymentMethod] = None
    transaction_id: Optional[str] = None
    receipt_url: Optional[str] = None
    paid_at: Optional[date] = None
    due_date: Optional[date] = None


class PaymentResponse(BaseResponse):
    payment: Optional[PaymentDTO] = None
    payments: Optional[List[PaymentDTO]] = None

    model_config = ConfigDict(from_attributes=True)