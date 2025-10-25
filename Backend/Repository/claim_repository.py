from sqlalchemy.orm import Session
from Entity.ClaimEntity import ClaimEntity
from Utils.Enums import EntityStatus


def find_active_claim_by_id(db_session: Session, claim_id: int):
    return db_session.query(ClaimEntity).filter(
        ClaimEntity.id == claim_id, ClaimEntity.entity_status == EntityStatus.ACTIVE).first()


def find_active_claim_by_claim_number(db_session: Session, claim_number: str):
    return db_session.query(ClaimEntity).filter(
        ClaimEntity.claim_number == claim_number, ClaimEntity.entity_status == EntityStatus.ACTIVE).first()


def find_active_claim_by_policy_id(db_session: Session, policy_id: int):
    return db_session.query(ClaimEntity).filter(
        ClaimEntity.policy_id == policy_id, ClaimEntity.entity_status == EntityStatus.ACTIVE).first()


def find_active_claim_by_user_id(db_session: Session, user_id: int):
    return db_session.query(ClaimEntity).filter(
        ClaimEntity.user_id == user_id, ClaimEntity.entity_status == EntityStatus.ACTIVE).first()


def find_all_active_claims(db_session: Session):
    return db_session.query(ClaimEntity).filter(ClaimEntity.entity_status == EntityStatus.ACTIVE).all()

def find_all_active_user_claims(db_session: Session, user_id: int):
    return db_session.query(ClaimEntity).filter(
        ClaimEntity.user_id == user_id,
        ClaimEntity.entity_status == EntityStatus.ACTIVE).all()