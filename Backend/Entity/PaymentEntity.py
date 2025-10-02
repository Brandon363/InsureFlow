from datetime import datetime

from sqlalchemy import Column, String, Enum, Date, Float, ForeignKey, DateTime, Integer
from sqlalchemy.orm import relationship

from Config.database import Base
from Utils.Enums import PaymentStatus, PaymentMethod, EntityStatus


class PaymentEntity(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    policy_id = Column(Integer, ForeignKey("policies.id"))
    amount = Column(Float)
    status = Column(Enum(PaymentStatus))
    payment_method = Column(Enum(PaymentMethod))
    transaction_id = Column(String(50))
    receipt_url = Column(String(255), nullable=True)
    paid_at = Column(Date)
    due_date = Column(Date)

    date_created = Column(DateTime, default=datetime.utcnow, nullable=True)
    date_updated = Column(DateTime, onupdate=datetime.utcnow, nullable=True)
    entity_status = Column(Enum(EntityStatus), nullable=False, default=EntityStatus.ACTIVE)

    user = relationship("UserEntity", back_populates="payments")
    policy = relationship("PolicyEntity", back_populates="payments")