from sqlalchemy.orm import Session

from Entity.ExtractedDependentEntity import ExtractedDependentEntity
from Entity.ExtractedTemporaryLossApplicationEntity import ExtractedTemporaryLossApplicationEntity
from Utils.Enums import EntityStatus



def find_active_extracted_dependent_by_id(db_session: Session, extracted_dependent_id: int):
    return db_session.query(ExtractedDependentEntity).filter(
        ExtractedDependentEntity.id == extracted_dependent_id,
        ExtractedDependentEntity.entity_status == EntityStatus.ACTIVE,
    ).first()


def find_active_extracted_dependents_by_application_id(db_session: Session, extracted_application_id: int):
    return db_session.query(ExtractedDependentEntity).filter(
        ExtractedDependentEntity.extracted_application_id == extracted_application_id,
        ExtractedDependentEntity.entity_status == EntityStatus.ACTIVE,
    ).all()


def find_all_active_extracted_dependents(db_session: Session):
    return db_session.query(ExtractedDependentEntity).filter(ExtractedDependentEntity.entity_status == EntityStatus.ACTIVE).all()