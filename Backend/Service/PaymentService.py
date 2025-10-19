from sqlalchemy.orm import Session
from Model.PaymentModel import PaymentCreate, PaymentUpdate, PaymentResponse, PaymentDTO
from Entity.PaymentEntity import PaymentEntity
from Repository import payment_repository
from Utils.Enums import EntityStatus
from datetime import datetime


def get_active_payment_by_id(db_session: Session, payment_id: int) -> PaymentResponse:
    if payment_id is None:
        return PaymentResponse(status_code=400, success=False, message="Payment ID cannot be null")

    payment = payment_repository.find_active_payment_by_id(db_session, payment_id)
    if not payment:
        return PaymentResponse(status_code=404, success=False, message=f"Payment with ID {payment_id} not found")

    return PaymentResponse(status_code=200, success=True, message="Payment successfully found", payment=payment)


def get_active_payment_by_user_id(db_session: Session, user_id: int) -> PaymentResponse:
    if user_id is None:
        return PaymentResponse(status_code=400, success=False, message="User ID cannot be null")

    payment = payment_repository.find_active_payment_by_user_id(db_session, user_id)
    if not payment:
        return PaymentResponse(status_code=404, success=False, message=f"No payment found for user ID {user_id}")

    return PaymentResponse(status_code=200, success=True, message="Payments successfully found", payment=payment)


def get_active_payment_by_policy_id(db_session: Session, policy_id: int) -> PaymentResponse:
    if policy_id is None:
        return PaymentResponse(status_code=400, success=False, message="Policy ID cannot be null")

    payment = payment_repository.find_active_payment_by_policy_id(db_session, policy_id)
    if not payment:
        return PaymentResponse(status_code=404, success=False, message=f"No payment found for policy ID {policy_id}")

    return PaymentResponse(status_code=200, success=True, message="Payments successfully found", payment=payment)


def get_all_active_payments(db_session: Session) -> PaymentResponse:
    payments = payment_repository.find_all_active_payments(db_session)
    if not payments:
        return PaymentResponse(status_code=404, success=False, message="No payments found")

    return PaymentResponse(status_code=200, success=True, message="Payments successfully found", payments=payments)


def create_payment(db_session: Session, create_request: PaymentCreate) -> PaymentResponse:
    new_payment = PaymentEntity(
        user_id=create_request.user_id,
        policy_id=create_request.policy_id,
        amount=create_request.amount,
        status=create_request.status,
        payment_method=create_request.payment_method,
        transaction_id=create_request.transaction_id,
        receipt_url=create_request.receipt_url,
        paid_at=create_request.paid_at,
        due_date=create_request.due_date,
        entity_status=EntityStatus.ACTIVE
    )

    db_session.add(new_payment)
    db_session.commit()
    db_session.refresh(new_payment)

    return PaymentResponse(status_code=201, success=True, message="Payment created successfully", payment=new_payment)


def update_payment(db_session: Session, payment_id: int, update_request: PaymentUpdate) -> PaymentResponse:
    if payment_id is None:
        return PaymentResponse(status_code=400, success=False, message="Payment ID cannot be null")

    payment = payment_repository.find_active_payment_by_id(db_session, payment_id)
    if not payment:
        return PaymentResponse(status_code=404, success=False, message=f"Payment with ID {payment_id} not found")

    update_dict = update_request.dict(exclude_unset=True)

    for key, value in update_dict.items():
        if value is not None and hasattr(payment, key):
            setattr(payment, key, value)

    payment.date_updated = datetime.utcnow()

    db_session.commit()
    db_session.refresh(payment)

    return PaymentResponse(status_code=200, success=True, message="Payment updated successfully", payment=payment)


def delete_payment(db_session: Session, payment_id: int) -> PaymentResponse:
    if payment_id is None:
        return PaymentResponse(status_code=400, success=False, message="Payment ID cannot be null")

    payment = payment_repository.find_active_payment_by_id(db_session, payment_id)
    if not payment:
        return PaymentResponse(status_code=404, success=False, message=f"Payment with ID {payment_id} not found")

    payment.entity_status = EntityStatus.DELETED
    payment.date_updated = datetime.utcnow()

    db_session.commit()

    return PaymentResponse(status_code=200, success=True, message="Payment successfully deleted", payment=payment)