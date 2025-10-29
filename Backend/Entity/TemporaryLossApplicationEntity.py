from datetime import datetime
from sqlalchemy import Column, String, Enum as SQLEnum, Date, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from Config.database import Base
from Utils.Enums import ApplicationStatus, EntityStatus


class TemporaryLossApplicationEntity(Base):
    __tablename__ = "temporary_loss_applications"

    id = Column(Integer, primary_key=True, index=True)
    # application_number = Column(String(50), unique=True, index=True)
    # extracted_application_id = Column(Integer, ForeignKey("extracted_temporary_loss_applications.id"))
    full_name = Column(String(100))
    id_number = Column(String(50))
    date_of_birth = Column(Date)
    contact_number = Column(String(20))
    email = Column(String(100))
    address = Column(String(255))
    nok_full_name = Column(String(100))
    nok_contact_number = Column(String(20))
    bank_name = Column(String(50))
    account_number = Column(String(50))
    branch_code = Column(String(10))
    existing_insurance_with_other_company = Column(String(100))
    existing_chronic_condition = Column(String(100))
    agent_full_name = Column(String(100))
    agent_number = Column(String(50))
    title = Column(String(20))
    gender = Column(String(10))
    b_date_of_birth = Column(Date)
    claim_ailment = Column(String(100))
    claim_amount = Column(String(50))
    declined_coverage = Column(String(10))
    declined_cover_reason = Column(String(100))

    status = Column(SQLEnum(ApplicationStatus), nullable=False, default=ApplicationStatus.PENDING)

    entity_status = Column(SQLEnum(EntityStatus), nullable=False, default=EntityStatus.ACTIVE)
    date_created = Column(DateTime, default=datetime.utcnow, nullable=True)
    date_updated = Column(DateTime, onupdate=datetime.utcnow, nullable=True)

    dependents = relationship("DependentEntity", back_populates="application")
    extracted_applications = relationship("ExtractedTemporaryLossApplicationEntity", back_populates="application")
    application_tracking_stages = relationship("ApplicationTrackingEntity", back_populates="application")
