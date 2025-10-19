from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Config.database import get_db
from Model.PaymentModel import PaymentResponse, PaymentCreate, PaymentUpdate
from Service import PaymentService

router = APIRouter(
    prefix="/payment"
)

db_dependency = Annotated[Session, Depends(get_db)]


@router.get('/get-active-payment-by-id/{payment_id}', response_model=PaymentResponse)
def get_active_payment_by_id(payment_id: int, db: db_dependency):
    return PaymentService.get_active_payment_by_id(db_session=db, payment_id=payment_id)


@router.get('/get-active-payment-by-user_id/{user_id}', response_model=PaymentResponse)
def get_active_payment_by_user_id(user_id: int, db: db_dependency):
    return PaymentService.get_active_payment_by_user_id(db_session=db, user_id=user_id)


@router.get('/get-active-payment-by-policy/{policy_id}', response_model=PaymentResponse)
def get_active_payment_by_policy_id(policy_id: int, db: db_dependency):
    return PaymentService.get_active_payment_by_policy_id(db_session=db, policy_id=policy_id)


@router.get('/get-all-active-payments', response_model=PaymentResponse)
def get_all_active_payments(db: db_dependency):
    return PaymentService.get_all_active_payments(db_session=db)


@router.post('/create-payment', response_model=PaymentResponse)
def create_payment(create_request: PaymentCreate, db: db_dependency):
    return PaymentService.create_payment(db_session=db, create_request=create_request)


@router.put('/update-payment/{payment_id}', response_model=PaymentResponse)
def update_payment(update_request: PaymentUpdate, payment_id: int, db: db_dependency):
    return PaymentService.update_payment(db_session=db, payment_id=payment_id, update_request=update_request)


@router.delete('/delete-payment/{payment_id}', response_model=PaymentResponse)
def delete_payment(payment_id: int, db: db_dependency):
    return PaymentService.delete_payment(db_session=db, payment_id=payment_id)