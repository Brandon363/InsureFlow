from sqlalchemy.orm import Session
from Entity.TemporaryLossApplicationEntity import TemporaryLossApplicationEntity
from Utils.Enums import EntityStatus


def find_temporary_loss_application_by_id(db_session: Session, application_id: int):
    return db_session.query(TemporaryLossApplicationEntity).filter(
        TemporaryLossApplicationEntity.id == application_id,
        TemporaryLossApplicationEntity.entity_status == EntityStatus.ACTIVE).first()


def find_temporary_loss_application_by_application_number(db_session: Session, application_number: str):
    return db_session.query(TemporaryLossApplicationEntity).filter(
        TemporaryLossApplicationEntity.application_number == application_number,
        TemporaryLossApplicationEntity.entity_status == EntityStatus.ACTIVE).first()


def find_all_temporary_loss_applications(db_session: Session):
    return db_session.query(TemporaryLossApplicationEntity).filter(
        TemporaryLossApplicationEntity.entity_status == EntityStatus.ACTIVE).all()


def find_all_user_temporary_loss_applications(db_session: Session, id_number:str):
    return db_session.query(TemporaryLossApplicationEntity).filter(
        TemporaryLossApplicationEntity.entity_status == EntityStatus.ACTIVE,
        TemporaryLossApplicationEntity.id_number == id_number).all()


def find_temporary_loss_applications_by_status(db_session: Session, status):
    return db_session.query(TemporaryLossApplicationEntity).filter(
        TemporaryLossApplicationEntity.status == status,
        TemporaryLossApplicationEntity.entity_status == EntityStatus.ACTIVE).all()