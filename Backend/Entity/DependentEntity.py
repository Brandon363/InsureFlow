from datetime import datetime

from sqlalchemy import Column, String, Enum as SQLEnum, Date, Float, JSON, ForeignKey, DateTime, Integer
from sqlalchemy.orm import relationship

from Config.database import Base
from Utils.Enums import PolicyType, PolicyStatus, EntityStatus


class DependentEntity(Base):
    __tablename__ = "dependents"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("temporary_loss_applications.id"))
    full_name = Column(String(100))
    id_number = Column(String(50))
    date_of_birth = Column(Date)
    age = Column(Integer)
    gender = Column(String(10))
    client_relationship = Column(String(50))

    entity_status = Column(SQLEnum(EntityStatus), nullable=False, default=EntityStatus.ACTIVE)
    date_created = Column(DateTime, default=datetime.utcnow, nullable=True)
    date_updated = Column(DateTime, onupdate=datetime.utcnow, nullable=True)

    application = relationship("TemporaryLossApplicationEntity", back_populates="dependents")