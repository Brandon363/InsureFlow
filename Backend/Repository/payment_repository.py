from sqlalchemy.orm import Session
from Entity.PaymentEntity import PaymentEntity
from Utils.Enums import EntityStatus


def find_active_payment_by_id(db_session: Session, payment_id: int):
    return db_session.query(PaymentEntity).filter(
        PaymentEntity.id == payment_id, PaymentEntity.entity_status == EntityStatus.ACTIVE).first()


def find_active_payment_by_user_id(db_session: Session, user_id: int):
    return db_session.query(PaymentEntity).filter(
        PaymentEntity.user_id == user_id, PaymentEntity.entity_status == EntityStatus.ACTIVE).first()


def find_active_payment_by_policy_id(db_session: Session, policy_id: int):
    return db_session.query(PaymentEntity).filter(
        PaymentEntity.policy_id == policy_id, PaymentEntity.entity_status == EntityStatus.ACTIVE).first()

def find_all_active_payments(db_session: Session):
    return db_session.query(PaymentEntity).filter(
        PaymentEntity.entity_status == EntityStatus.ACTIVE).all()

