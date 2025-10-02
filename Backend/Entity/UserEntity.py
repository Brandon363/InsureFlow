from sqlalchemy import Column, String, Enum, Date, DateTime, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from Config.database import Base
from sqlalchemy.orm import relationship

from Entity.ClaimEntity import ClaimEntity
from Utils.Enums import UserRole, EntityStatus

class UserEntity(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    id_number = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True)
    village_of_origin = Column(String(100))
    place_of_birth = Column(String(100))
    password = Column(String(255))
    first_name = Column(String(100))
    last_name = Column(String(100))
    role = Column(Enum(UserRole))
    phone_number = Column(String(20), nullable=True)
    address = Column(String(255), nullable=True)
    date_of_birth = Column(Date, nullable=False)
    is_logged_in = Column(Boolean, nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow, nullable=True)
    date_updated = Column(DateTime, onupdate=datetime.utcnow, nullable=True)
    entity_status = Column(Enum(EntityStatus), nullable=False, default=EntityStatus.ACTIVE)

    agent = relationship("AgentEntity", back_populates="user")
    policies = relationship("PolicyEntity", back_populates="user")
    claims = relationship("ClaimEntity", foreign_keys=[ClaimEntity.user_id], back_populates="user")
    payments = relationship("PaymentEntity", back_populates="user")
    documents = relationship("DocumentEntity", back_populates="user")
    notifications = relationship("NotificationEntity", back_populates="user")