from sqlalchemy.orm import Session
from Entity.UserEntity import UserEntity
from Utils.Enums import EntityStatus


def find_active_user_by_id(db_session: Session, user_id: int):
    return db_session.query(UserEntity).filter(
        UserEntity.id == user_id, UserEntity.entity_status == EntityStatus.ACTIVE).first()


def find_active_user_by_id_number(db_session: Session, id_number: str):
    return db_session.query(UserEntity).filter(
        UserEntity.id_number == id_number, UserEntity.entity_status == EntityStatus.ACTIVE).first()


def find_all_active_users(db_session: Session):
    return db_session.query(UserEntity).filter(UserEntity.entity_status == EntityStatus.ACTIVE).all()