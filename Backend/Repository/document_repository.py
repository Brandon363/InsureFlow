from sqlalchemy.orm import Session
from Entity.DocumentEntity import DocumentEntity
from Utils.Enums import EntityStatus


def find_active_document_by_id(db_session: Session, document_id: int):
    return db_session.query(DocumentEntity).filter(
        DocumentEntity.id == document_id, DocumentEntity.entity_status == EntityStatus.ACTIVE).first()


def find_active_document_by_user_id(db_session: Session, user_id: int):
    return db_session.query(DocumentEntity).filter(
        DocumentEntity.user_id == user_id, DocumentEntity.entity_status == EntityStatus.ACTIVE).first()


def find_active_document_by_claim_id(db_session: Session, claim_id: int):
    return db_session.query(DocumentEntity).filter(
        DocumentEntity.claim_id == claim_id, DocumentEntity.entity_status == EntityStatus.ACTIVE).first()


def find_active_document_by_policy_id(db_session: Session, policy_id: int):
    return db_session.query(DocumentEntity).filter(
        DocumentEntity.policy_id == policy_id, DocumentEntity.entity_status == EntityStatus.ACTIVE).first()


def find_all_active_claims(db_session: Session):
    return db_session.query(DocumentEntity).filter(DocumentEntity.entity_status == EntityStatus.ACTIVE).all()