from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from Model.ResponseModel import BaseResponse
from Utils.Enums import EntityStatus


class ExtractedUserDTO(BaseModel):
    id: int
    user_id: int
    id_number: Optional[str] = None
    id_number_confidence: Optional[float] = None
    first_name: Optional[str] = None
    first_name_confidence: Optional[float] = None
    other_names: Optional[str] = None
    other_names_confidence: Optional[float] = None
    last_name: Optional[str] = None
    last_name_confidence: Optional[float] = None
    village_of_origin: Optional[str] = None
    village_of_origin_confidence: Optional[float] = None
    place_of_birth: Optional[str] = None
    place_of_birth_confidence: Optional[float] = None
    address: Optional[str] = None
    address_confidence: Optional[float] = None
    date_of_birth: Optional[date] = None
    date_of_birth_confidence: Optional[float] = None
    overall_accuracy: Optional[float] = None
    date_created: Optional[datetime] = None
    date_updated: Optional[datetime] = None
    entity_status: EntityStatus

    model_config = ConfigDict(from_attributes=True)


class ExtractedUserCreateRequest(BaseModel):
    user_id: int
    id_number: Optional[str] = None
    id_number_confidence: Optional[float] = None
    first_name: Optional[str] = None
    first_name_confidence: Optional[float] = None
    other_names: Optional[str] = None
    other_names_confidence: Optional[float] = None
    last_name: Optional[str] = None
    last_name_confidence: Optional[float] = None
    village_of_origin: Optional[str] = None
    village_of_origin_confidence: Optional[float] = None
    place_of_birth: Optional[str] = None
    place_of_birth_confidence: Optional[float] = None
    address: Optional[str] = None
    address_confidence: Optional[float] = None
    overall_accuracy: Optional[float] = None
    date_of_birth: Optional[date] = None
    date_of_birth_confidence: Optional[float] = None


class ExtractedUserUpdateRequest(BaseModel):
    id: int
    user_id: Optional[int] = None
    id_number: Optional[str] = None
    id_number_confidence: Optional[float] = None
    first_name: Optional[str] = None
    first_name_confidence: Optional[float] = None
    other_names: Optional[str] = None
    other_names_confidence: Optional[float] = None
    last_name: Optional[str] = None
    last_name_confidence: Optional[float] = None
    village_of_origin: Optional[str] = None
    village_of_origin_confidence: Optional[float] = None
    place_of_birth: Optional[str] = None
    place_of_birth_confidence: Optional[float] = None
    address: Optional[str] = None
    address_confidence: Optional[float] = None
    date_of_birth: Optional[date] = None
    date_of_birth_confidence: Optional[float] = None
    overall_accuracy: Optional[float] = None
    entity_status: Optional[EntityStatus] = None


class ExtractedUserResponse(BaseResponse):
    extracted_user: Optional[ExtractedUserDTO] = None
    extracted_users: Optional[List[ExtractedUserDTO]] = None