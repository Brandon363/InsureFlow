from sqlalchemy.orm import Session
from Entity.NotificationEntity import NotificationEntity
from Utils.Enums import EntityStatus


def find_active_notification_by_id(db_session: Session, notification_id: int):
    return db_session.query(NotificationEntity).filter(
        NotificationEntity.id == notification_id, NotificationEntity.entity_status == EntityStatus.ACTIVE).first()


def find_active_notification_by_claim_id(db_session: Session, claim_id: int):
    return db_session.query(NotificationEntity).filter(
        NotificationEntity.claim_id == claim_id, NotificationEntity.entity_status == EntityStatus.ACTIVE).first()


def find_active_notifications_by_user_id(db_session: Session, user_id: int):
    return db_session.query(NotificationEntity).filter(
        NotificationEntity.user_id == user_id, NotificationEntity.entity_status == EntityStatus.ACTIVE).all()


def find_unread_notifications_by_user_id(db_session: Session, user_id: int):
    return db_session.query(NotificationEntity).filter(
        NotificationEntity.user_id == user_id, NotificationEntity.is_read == False,
        NotificationEntity.entity_status == EntityStatus.ACTIVE).all()


def find_all_active_notifications(db_session: Session):
    return db_session.query(NotificationEntity).filter(NotificationEntity.entity_status == EntityStatus.ACTIVE).all()
