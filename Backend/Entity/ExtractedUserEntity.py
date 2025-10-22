from sqlalchemy import Column, String, Enum, Date, DateTime, Integer, Boolean, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from Config.database import Base
from sqlalchemy.orm import relationship
from Utils.password_utils import hash_password, verify_password
from Entity.ClaimEntity import ClaimEntity
from Utils.Enums import UserRole, EntityStatus



class ExtractedUserEntity(Base):
    __tablename__ = "extracted_user_data"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    id_number = Column(String(50))
    id_number_confidence = Column(Float)
    first_name = Column(String(100))
    first_name_confidence = Column(Float)
    other_names = Column(String(100))
    other_names_confidence = Column(Float)
    last_name = Column(String(100))
    last_name_confidence = Column(Float)
    village_of_origin = Column(String(100))
    village_of_origin_confidence = Column(Float)
    place_of_birth = Column(String(100))
    place_of_birth_confidence = Column(Float)
    address = Column(String(255))
    address_confidence = Column(Float)
    date_of_birth = Column(Date)
    date_of_birth_confidence = Column(Float)
    overall_accuracy = Column(Float)

    date_created = Column(DateTime, default=datetime.utcnow, nullable=True)
    date_updated = Column(DateTime, onupdate=datetime.utcnow, nullable=True)
    entity_status = Column(Enum(EntityStatus), nullable=False, default=EntityStatus.ACTIVE)

    user = relationship("UserEntity", back_populates="extracted_user", uselist=False)
    # document = relationship("DocumentEntity", back_populates="extracted_user", uselist=False)