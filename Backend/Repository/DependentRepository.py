from sqlalchemy.orm import Session
from Entity.DependentEntity import DependentEntity
from Utils.Enums import EntityStatus


def find_dependent_by_id(db_session: Session, dependent_id: int):
    return db_session.query(DependentEntity).filter(
        DependentEntity.id == dependent_id,
        DependentEntity.entity_status == EntityStatus.ACTIVE).first()


def find_dependents_by_application_id(db_session: Session, application_id: int):
    return db_session.query(DependentEntity).filter(
        DependentEntity.application_id == application_id,
        DependentEntity.entity_status == EntityStatus.ACTIVE).all()


def find_all_dependents(db_session: Session):
    return db_session.query(DependentEntity).filter(
        DependentEntity.entity_status == EntityStatus.ACTIVE).all()