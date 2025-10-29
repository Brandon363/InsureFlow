from sqlalchemy.orm import Session
from Entity.ExtractedTemporaryLossApplicationEntity import ExtractedTemporaryLossApplicationEntity
from Utils.Enums import EntityStatus


def find_extracted_temporary_loss_application_by_id(db_session: Session, id: int):
    return db_session.query(ExtractedTemporaryLossApplicationEntity).filter(
        ExtractedTemporaryLossApplicationEntity.id == id,
        ExtractedTemporaryLossApplicationEntity.entity_status == EntityStatus.ACTIVE).first()


def find_all_extracted_temporary_loss_applications(db_session: Session):
    return db_session.query(ExtractedTemporaryLossApplicationEntity).filter(
        ExtractedTemporaryLossApplicationEntity.entity_status == EntityStatus.ACTIVE).all()