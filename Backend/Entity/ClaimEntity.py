from datetime import datetime

from sqlalchemy import Column, String, Enum as SQLEnum, Date, Float, JSON, ForeignKey, DateTime,Integer
from sqlalchemy.orm import relationship

from Config.database import Base
from Utils.Enums import ClaimStatus, EntityStatus


class ClaimEntity(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)
    claim_number = Column(String(50), unique=True, index=True)
    policy_id = Column(Integer, ForeignKey("policies.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String(50))
    status = Column(SQLEnum(ClaimStatus))
    description = Column(String(255))
    incident_date = Column(Date)
    amount = Column(Float)
    notes = Column(String(255), nullable=True)
    approved_amount = Column(Float, nullable=True)
    processed_at = Column(Date, nullable=True)
    processed_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    date_created = Column(DateTime, default=datetime.utcnow, nullable=True)
    date_updated = Column(DateTime, onupdate=datetime.utcnow, nullable=True)
    entity_status = Column(SQLEnum(EntityStatus), nullable=False, default=EntityStatus.ACTIVE)

    policy = relationship("PolicyEntity", back_populates="claims")
    documents = relationship("DocumentEntity", back_populates="claim")
    user = relationship("UserEntity", foreign_keys=[user_id], back_populates="claims")
    notifications = relationship("NotificationEntity", back_populates="claim")
    processed_by_user = relationship("UserEntity", foreign_keys=[processed_by])