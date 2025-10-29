from pydantic import BaseModel, ConfigDict, field_validator
from datetime import date, datetime
from typing import Optional, List
from Utils.Validators import strip_string, capitalize_field, clean_id_number, normalize_email

from Model.ExtractedUserModel import ExtractedUserDTO
from Model.ResponseModel import BaseResponse
from Utils.Enums import UserRole, EntityStatus, VerificationStatus


class UserDTO(BaseModel):
    id: int
    id_number: str
    email: str
    first_name: str
    other_names: Optional[str] = None
    last_name: str
    user_role: UserRole
    date_of_birth: date
    village_of_origin: str
    place_of_birth: str
    phone_number: Optional[str] = None
    address: Optional[str]
    is_logged_in: bool
    date_last_logged_in: Optional[datetime] = None
    # is_verified: bool
    verification_notes: Optional[str] = None
    verification_status: VerificationStatus
    date_created: datetime
    date_updated: Optional[datetime] = None
    entity_status: EntityStatus
    extracted_users: Optional[List[ExtractedUserDTO]] = None

    model_config = ConfigDict(from_attributes=True)


class UserCreateRequest(BaseModel):
    id_number: str #
    email: str
    first_name: str #
    last_name: str #
    other_names: Optional[str] = None
    user_role: UserRole
    date_of_birth: date #
    village_of_origin: str #
    place_of_birth: str
    phone_number: Optional[str] = None #
    address: Optional[str] = None
    password: str

    @field_validator('*', mode='before')
    def strip_fields(cls, v, info):
        return strip_string(v, skip_fields=['password'], field_name=info.field_name)

    @field_validator('first_name', 'last_name', 'other_names', 'village_of_origin', 'place_of_birth', 'address',
                     mode='before')
    def capitalize_fields(cls, v):
        return capitalize_field(v)

    @field_validator('id_number', mode='before')
    def format_id_number(cls, v):
        return clean_id_number(v)

    @field_validator('email', mode='before')
    def normalize_email_field(cls, v):
        return normalize_email(v)


class UserUpdateRequest(BaseModel):
    id: int
    id_number: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    other_names: Optional[str] = None
    # user_role: Optional[UserRole] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[date] = None
    village_of_origin: Optional[str] = None
    place_of_birth: Optional[str] = None
    is_logged_in: Optional[bool] = None
    date_last_logged_in: Optional[datetime] = None

    @field_validator('*', mode='before')
    def strip_fields(cls, v, info):
        return strip_string(v, skip_fields=['password'], field_name=info.field_name)

    @field_validator('first_name', 'last_name', 'other_names', 'village_of_origin', 'place_of_birth', 'address',
                     mode='before')
    def capitalize_fields(cls, v):
        return capitalize_field(v)

    @field_validator('id_number', mode='before')
    def format_id_number(cls, v):
        return clean_id_number(v)

    @field_validator('email', mode='before')
    def normalize_email_field(cls, v):
        return normalize_email(v)


class UserResponse(BaseResponse):
    user: Optional[UserDTO] = None
    users: Optional[List[UserDTO]] = None

class UserLoginRequest(BaseModel):
    email: str
    password: str


class UserVerificationRequest(BaseModel):
    user_id: int
    verifier_id: int
    verification_notes: str


class UserPasswordUpdate(BaseModel):
    old_password: str
    new_password: str



