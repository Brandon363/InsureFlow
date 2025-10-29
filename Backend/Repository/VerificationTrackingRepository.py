from sqlalchemy.orm import Session
from Entity.VerificationTrackingEntity import VerificationTrackingEntity
from Utils.Enums import EntityStatus


def find_verification_tracking_by_id(db_session: Session, verification_tracking_id: int):
    return db_session.query(VerificationTrackingEntity).filter(
        VerificationTrackingEntity.id == verification_tracking_id,
        ).first()


def find_verification_trackings_by_user_id(db_session: Session, user_id: int):
    return db_session.query(VerificationTrackingEntity).filter(
        VerificationTrackingEntity.user_id == user_id,
        ).all()


def find_all_verification_trackings(db_session: Session):
    return db_session.query(VerificationTrackingEntity).filter(
        ).all()