from datetime import datetime

from sqlalchemy import Column, String, Enum, Date, DateTime, Integer, Boolean, inspect
from sqlalchemy.orm import relationship, validates

from Config.database import Base
from Entity.ClaimEntity import ClaimEntity
from Utils.Enums import UserRole, EntityStatus, VerificationStatus
from Utils.password_utils import hash_password, verify_password


class UserEntity(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    id_number = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True)
    village_of_origin = Column(String(100), nullable=False)
    place_of_birth = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    other_names = Column(String(100), nullable=True)
    user_role = Column(Enum(UserRole), nullable=False)
    phone_number = Column(String(20), nullable=True)
    address = Column(String(255), nullable=True)
    date_of_birth = Column(Date, nullable=False)
    is_logged_in = Column(Boolean, default=False, nullable=False)
    date_last_logged_in = Column(DateTime, nullable=True)
    verification_notes = Column(String(2000), nullable=True)
    verification_status = Column(Enum(VerificationStatus), nullable=False, default=VerificationStatus.UNVERIFIED)
    date_created = Column(DateTime, default=datetime.utcnow, nullable=True)
    date_updated = Column(DateTime, onupdate=datetime.utcnow, nullable=True)
    entity_status = Column(Enum(EntityStatus), nullable=False, default=EntityStatus.ACTIVE)

    agent = relationship("AgentEntity", back_populates="user", uselist=False)
    policies = relationship("PolicyEntity", back_populates="user")
    claims = relationship("ClaimEntity", foreign_keys=[ClaimEntity.user_id], back_populates="user")
    payments = relationship("PaymentEntity", back_populates="user")
    documents = relationship("DocumentEntity", back_populates="user")
    notifications = relationship("NotificationEntity", back_populates="user")
    extracted_users = relationship("ExtractedUserEntity", back_populates="user")

    # application_tracking_actions = relationship("ApplicationTrackingEntity", back_populates="user")

    # tracked_application_tracking = relationship("ApplicationTrackingEntity",
    #                                             foreign_keys="[ApplicationTrackingEntity.user_id]",
    #                                             back_populates="user")
    performed_application_tracking = relationship("ApplicationTrackingEntity",
                                                  foreign_keys="[ApplicationTrackingEntity.action_performed_by_id]",
                                                  back_populates="action_performed_by")

    tracked_verification_tracking = relationship("VerificationTrackingEntity",
                                                foreign_keys="[VerificationTrackingEntity.user_id]",
                                                back_populates="user")
    performed_verification_tracking = relationship("VerificationTrackingEntity",
                                                  foreign_keys="[VerificationTrackingEntity.action_performed_by_id]",
                                                  back_populates="action_performed_by")


    def set_password(self, password: str):
        # Hash and set the password
        self.password = hash_password(password)

    def check_password(self, password: str) -> bool:
        # Check if the provided password matches the hashed password
        return verify_password(password, self.password)


    @validates('*')
    def validate_string_fields(self, key, value):
        if key in inspect(self.__class__).column_attrs and isinstance(value, str) and key != 'password':
            return value.strip()
        return value

    @validates('first_name', 'last_name', 'other_names', 'village_of_origin', 'place_of_birth', 'address')
    def validate_string_fields(self, key, value):
        return value.capitalize()

    @validates('id_number')
    def validate_string_fields(self, key, value):
        return value.replace(" ", "")
