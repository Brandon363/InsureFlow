from sqlalchemy.orm import Session
from Entity.PolicyEntity import PolicyEntity
from Utils.Enums import EntityStatus


def find_active_policy_by_id(db_session: Session, policy_id: int):
    return db_session.query(PolicyEntity).filter(
        PolicyEntity.id == policy_id, PolicyEntity.entity_status == EntityStatus.ACTIVE).first()


def find_active_policy_by_policy_number(db_session: Session, policy_number: str):
    return db_session.query(PolicyEntity).filter(
        PolicyEntity.policy_number == policy_number, PolicyEntity.entity_status == EntityStatus.ACTIVE).first()


def find_active_policy_by_user_id(db_session: Session, user_id: int):
    return db_session.query(PolicyEntity).filter(
        PolicyEntity.user_id == user_id, PolicyEntity.entity_status == EntityStatus.ACTIVE).first()


def find_all_active_policies(db_session: Session):
    return db_session.query(PolicyEntity).filter(PolicyEntity.entity_status == EntityStatus.ACTIVE).all()