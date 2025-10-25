from sqlalchemy.orm import Session
from Entity.DocumentEntity import DocumentEntity
from Utils.Enums import EntityStatus, DocumentType


def find_active_document_by_id(db_session: Session, document_id: int):
    return db_session.query(DocumentEntity).filter(
        DocumentEntity.id == document_id, DocumentEntity.entity_status == EntityStatus.ACTIVE).first()


# def find_active_id_document_by_user_id(db_session: Session, user_id: int):
#     return db_session.query(DocumentEntity).filter(
#         DocumentEntity.user_id == user_id,
#         DocumentEntity.type == DocumentType.NATIONAL_ID,
#         DocumentEntity.entity_status == EntityStatus.ACTIVE).first()

def find_active_id_document_by_user_id(db_session: Session, user_id: int):
    return (
        db_session.query(DocumentEntity)
        .filter(
            DocumentEntity.user_id == user_id,
            DocumentEntity.type == DocumentType.NATIONAL_ID,
            DocumentEntity.entity_status == EntityStatus.ACTIVE,
        )
        .order_by(DocumentEntity.date_created.desc())
        .first()
    )


def find_all_active_documents(db_session: Session, skip: int = 0, limit: int = 100):
    return db_session.query(DocumentEntity).filter(
        DocumentEntity.entity_status == EntityStatus.ACTIVE).offset(skip).limit(limit).all()


def find_active_documents_by_user_id(db_session: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db_session.query(DocumentEntity).filter(
        DocumentEntity.user_id == user_id, DocumentEntity.entity_status == EntityStatus.ACTIVE).offset(skip).limit(
        limit).all()


def find_active_documents_by_claim_id(db_session: Session, claim_id: int, skip: int = 0, limit: int = 100):
    return db_session.query(DocumentEntity).filter(
        DocumentEntity.claim_id == claim_id, DocumentEntity.entity_status == EntityStatus.ACTIVE).offset(skip).limit(
        limit).all()


def find_active_documents_by_type(db_session: Session, document_type: str, skip: int = 0, limit: int = 100):
    return db_session.query(DocumentEntity).filter(
        DocumentEntity.type == document_type, DocumentEntity.entity_status == EntityStatus.ACTIVE).offset(skip).limit(
        limit).all()


def find_active_documents_by_policy_id(db_session: Session, policy_id: int, skip: int = 0, limit: int = 100):
    return db_session.query(DocumentEntity).filter(
        DocumentEntity.policy_id == policy_id, DocumentEntity.entity_status == EntityStatus.ACTIVE).offset(skip).limit(
        limit).all()
