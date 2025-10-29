from sqlalchemy.orm import Session
from Entity.ApplicationTrackingEntity import ApplicationTrackingEntity
from Utils.Enums import EntityStatus


def find_application_tracking_by_id(db_session: Session, application_tracking_id: int):
    return db_session.query(ApplicationTrackingEntity).filter(
        ApplicationTrackingEntity.id == application_tracking_id,
        ApplicationTrackingEntity.entity_status == EntityStatus.ACTIVE).first()


def find_application_tracking_by_application_id(db_session: Session, application_id: int):
    return db_session.query(ApplicationTrackingEntity).filter(
        ApplicationTrackingEntity.application_id == application_id,
        ApplicationTrackingEntity.entity_status == EntityStatus.ACTIVE).first()


def find_application_trackings_by_application_id(db_session: Session, application_id: int):
    return db_session.query(ApplicationTrackingEntity).filter(
        ApplicationTrackingEntity.application_id == application_id,
        ApplicationTrackingEntity.entity_status == EntityStatus.ACTIVE).all()


def find_all_application_trackings(db_session: Session):
    return db_session.query(ApplicationTrackingEntity).filter(
        ApplicationTrackingEntity.entity_status == EntityStatus.ACTIVE).all()