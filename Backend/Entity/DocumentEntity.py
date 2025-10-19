from sqlalchemy import Column, String, Date, Float, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from Config.database import Base
from datetime import datetime

from Utils.Enums import EntityStatus

class DocumentEntity(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    claim_id = Column(Integer, ForeignKey("claims.id"), nullable=True)
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=True)
    type = Column(String(50))
    name = Column(String(100))
    url = Column(String(255))
    mime_type = Column(String(50))
    size = Column(Integer)
    date_created = Column(DateTime, default=datetime.utcnow, nullable=True)
    date_updated = Column(DateTime, onupdate=datetime.utcnow, nullable=True)
    entity_status = Column(Enum(EntityStatus), nullable=False, default=EntityStatus.ACTIVE)


    user = relationship("UserEntity", back_populates="documents")
    claim = relationship("ClaimEntity", back_populates="documents")
    policy = relationship("PolicyEntity", back_populates="documents")