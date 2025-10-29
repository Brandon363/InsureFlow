from datetime import datetime

from sqlalchemy import Column, String, Enum as SQLEnum, ForeignKey, DateTime, Integer
from sqlalchemy.orm import relationship

from Config.database import Base
from Utils.Enums import ApplicationStage, TrackingStatus


class ApplicationTrackingEntity(Base):
    __tablename__ = "application_tracking"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("temporary_loss_applications.id"))
    stage = Column(SQLEnum(ApplicationStage), nullable=False)
    status = Column(SQLEnum(TrackingStatus), nullable=False)
    date_created = Column(DateTime, nullable=False, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))  # User being tracked
    action_performed_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # User who performed the action
    notes = Column(String(500), nullable=True)

    # Relationship to the User entity
    user = relationship("UserEntity", foreign_keys=[user_id], back_populates="tracked_application_tracking")
    action_performed_by = relationship("UserEntity", foreign_keys=[action_performed_by_id], back_populates="performed_application_tracking")
    application = relationship("TemporaryLossApplicationEntity", back_populates="application_tracking_stages")