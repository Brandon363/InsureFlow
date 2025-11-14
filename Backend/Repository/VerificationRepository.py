from sqlalchemy.orm import Session
from Entity.UserEntity import UserEntity
from Utils.Enums import EntityStatus
from sqlalchemy import or_
from difflib import SequenceMatcher


def find_active_user_by_id_number(db_session: Session, id_number: str):
    return db_session.query(UserEntity).filter(
        UserEntity.id_number == id_number, UserEntity.entity_status == EntityStatus.ACTIVE).first()


def find_users_by_id_number_partial(db_session: Session, id_number: str):
    return db_session.query(UserEntity).filter(
        UserEntity.id_number.ilike(f"%{id_number}%"), UserEntity.entity_status == EntityStatus.ACTIVE).all()


def find_users_by_name_partial(db_session: Session, first_name: str, last_name: str):
    return db_session.query(UserEntity).filter(
        or_(UserEntity.first_name.ilike(f"%{first_name}%"), UserEntity.last_name.ilike(f"%{last_name}%")),
        UserEntity.entity_status == EntityStatus.ACTIVE).all()


def find_users_by_email_partial(db_session: Session, email: str):
    return db_session.query(UserEntity).filter(
        UserEntity.email.ilike(f"%{email}%"), UserEntity.entity_status == EntityStatus.ACTIVE).all()


def find_users_by_phone_partial(db_session: Session, phone_number: str):
    return db_session.query(UserEntity).filter(
        UserEntity.phone_number.ilike(f"%{phone_number}%"), UserEntity.entity_status == EntityStatus.ACTIVE ).all()


def find_users_by_fuzzy_id_number(db_session: Session, id_number: str):
    all_active_users = db_session.query(UserEntity).filter(
        UserEntity.entity_status == EntityStatus.ACTIVE).all()

    threshold = 0.7
    fuzzy_matches = [u for u in all_active_users if SequenceMatcher(None, u.id_number, id_number).ratio() >= threshold]
    return fuzzy_matches
