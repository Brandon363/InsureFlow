from sqlalchemy import Column, String, Enum, Boolean, ForeignKey, DateTime, Integer
from sqlalchemy.orm import relationship
from Config.database import Base
from datetime import datetime

from Utils.Enums import NotificationType, EntityStatus

class NotificationEntity(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(Enum(NotificationType))
    title = Column(String(100))
    message = Column(String(255))
    read = Column(Boolean, default=False)
    related_id = Column(Integer, nullable=True)

    date_created = Column(DateTime, default=datetime.utcnow, nullable=True)
    date_updated = Column(DateTime, onupdate=datetime.utcnow, nullable=True)
    entity_status = Column(Enum(EntityStatus), nullable=False, default=EntityStatus.ACTIVE)


    user = relationship("UserEntity", back_populates="notifications")