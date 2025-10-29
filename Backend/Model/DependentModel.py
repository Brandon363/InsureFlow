from datetime import datetime, date
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from Model.ResponseModel import BaseResponse


class DependentDTO(BaseModel):
    id: int
    application_id: int
    full_name: str
    id_number: str
    date_of_birth: date
    age: int
    gender: str
    client_relationship: str
    date_created: Optional[datetime]
    date_updated: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class DependentCreateRequest(BaseModel):
    application_id: int
    full_name: str
    id_number: str
    date_of_birth: date
    age: int
    gender: str
    client_relationship: str

    model_config = ConfigDict(from_attributes=True)


class DependentUpdateRequest(BaseModel):
    id: int
    application_id: Optional[int]
    full_name: Optional[str]
    id_number: Optional[str]
    date_of_birth: Optional[date]
    age: Optional[int]
    gender: Optional[str]
    client_relationship: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class DependentResponse(BaseResponse):
    dependent: Optional[DependentDTO] = None
    dependents: Optional[List[DependentDTO]] = None