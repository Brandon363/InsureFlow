from sqlalchemy import Column, String, Enum as SQLEnum, Date, DateTime, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from Config.database import Base
from Utils.Enums import EntityStatus, ApplicationStatus
from datetime import datetime

class ExtractedDependentEntity(Base):
    __tablename__ = "extracted_dependents"

    id = Column(Integer, primary_key=True, index=True)
    extracted_application_id = Column(Integer, ForeignKey("extracted_temporary_loss_applications.id"))
    full_name = Column(String(100))
    full_name_confidence = Column(Float)
    id_number = Column(String(50))
    id_number_confidence = Column(Float)
    date_of_birth = Column(Date)
    date_of_birth_confidence = Column(Float)
    age = Column(Integer)
    age_confidence = Column(Float)
    gender = Column(String(10))
    gender_confidence = Column(Float)
    client_relationship = Column(String(50))
    client_relationship_confidence = Column(Float)

    entity_status = Column(SQLEnum(EntityStatus), nullable=False, default=EntityStatus.ACTIVE)
    date_created = Column(DateTime, default=datetime.utcnow, nullable=True)
    date_updated = Column(DateTime, onupdate=datetime.utcnow, nullable=True)

    extracted_application = relationship("ExtractedTemporaryLossApplicationEntity", back_populates="extracted_dependents")