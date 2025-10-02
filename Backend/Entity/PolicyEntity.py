from datetime import datetime

from sqlalchemy import Column, String, Enum as SQLEnum, Date, Float, JSON, ForeignKey, DateTime, Integer
from sqlalchemy.orm import relationship

from Config.database import Base
from Utils.Enums import PolicyType, PolicyStatus, EntityStatus


class PolicyEntity(Base):
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True, index=True)
    policy_number = Column(String(50), unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(SQLEnum(PolicyType))
    status = Column(SQLEnum(PolicyStatus))
    start_date = Column(Date)
    end_date = Column(Date)
    premium = Column(Float)
    coverage = Column(Float)
    deductible = Column(Float)
    details = Column(JSON)
    date_created = Column(DateTime, default=datetime.utcnow, nullable=True)
    date_updated = Column(DateTime, onupdate=datetime.utcnow, nullable=True)
    entity_status = Column(SQLEnum(EntityStatus), nullable=False, default=EntityStatus.ACTIVE)


    user = relationship("UserEntity", back_populates="policies")
    claims = relationship("ClaimEntity", back_populates="policy")
    payments = relationship("PaymentEntity", back_populates="policy")
    # documents = relationship("DocumentEntity", back_populates="policy")