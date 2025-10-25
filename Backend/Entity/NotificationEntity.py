from sqlalchemy import Column, String, Enum, Boolean, ForeignKey, DateTime, Integer, Text
from sqlalchemy.orm import relationship
from Config.database import Base
from datetime import datetime

from Utils.Enums import NotificationType, NotificationStatus, EntityStatus

class NotificationEntity(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    claim_id = Column(Integer, ForeignKey("claims.id"), nullable=True)
    notification_type = Column(Enum(NotificationType), nullable=False)
    title = Column(String(800), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(Enum(NotificationStatus), default=NotificationStatus.UNREAD, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    read_at = Column(DateTime, nullable=True)
    related_id = Column(Integer, nullable=True)

    date_created = Column(DateTime, default=datetime.utcnow, nullable=True)
    date_updated = Column(DateTime, onupdate=datetime.utcnow, nullable=True)
    entity_status = Column(Enum(EntityStatus), nullable=False, default=EntityStatus.ACTIVE)


    user = relationship("UserEntity", back_populates="notifications")
    claim = relationship("ClaimEntity", back_populates="notifications")