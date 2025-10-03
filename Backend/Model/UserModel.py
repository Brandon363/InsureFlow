from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional, List

from Model.ResponseModel import BaseResponse
from Utils.Enums import UserRole, EntityStatus


class UserDTO(BaseModel):
    id: int
    id_number: str
    email: str
    first_name: str
    last_name: str
    role: UserRole
    date_of_birth: date
    village_of_origin: str
    place_of_birth: str
    phone_number: Optional[str] = None
    address: Optional[str]
    is_logged_in: bool
    date_created: datetime
    date_updated: Optional[datetime] = None
    entity_status: EntityStatus

    # class Config:
    #     from_attribute = True
    model_config = ConfigDict(from_attributes=True)


class UserCreateRequest(BaseModel):
    id_number: str
    email: str
    first_name: str
    last_name: str
    role: UserRole
    date_of_birth: date
    village_of_origin: str
    place_of_birth: str
    phone_number: Optional[str] = None
    address: Optional[str] = None
    password: str


class UserUpdateRequest(BaseModel):
    id: int
    id_number: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[UserRole] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[date] = None
    village_of_origin: Optional[str] = None
    place_of_birth: Optional[str] = None
    is_logged_in: Optional[bool] = None


class UserLoginRequest(BaseModel):
    email: str
    password: str


class UserPasswordUpdate(BaseModel):
    old_password: str
    new_password: str


class UserResponse(BaseResponse):
    user: Optional[UserDTO] = None
    users: Optional[List[UserDTO]] = None


