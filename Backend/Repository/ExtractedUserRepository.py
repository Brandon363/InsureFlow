from sqlalchemy.orm import Session
from Entity.ExtractedUserEntity import ExtractedUserEntity
from Utils.Enums import EntityStatus


def find_active_extracted_user_by_id(db_session: Session, extracted_user_id: int):
    return db_session.query(ExtractedUserEntity).filter(
        ExtractedUserEntity.id == extracted_user_id,
        ExtractedUserEntity.entity_status == EntityStatus.ACTIVE,
    ).first()


def find_active_extracted_user_by_user_id(db_session: Session, user_id: int):
    return (
        db_session.query(ExtractedUserEntity)
        .filter(
            ExtractedUserEntity.user_id == user_id,
            ExtractedUserEntity.entity_status == EntityStatus.ACTIVE,
        )
        .order_by(ExtractedUserEntity.date_created.desc())
        .first()
    )


def find_all_active_extracted_users(db_session: Session):
    return db_session.query(ExtractedUserEntity).filter(ExtractedUserEntity.entity_status == EntityStatus.ACTIVE).all()
