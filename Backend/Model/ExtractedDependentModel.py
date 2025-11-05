from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional, List

from Model.ResponseModel import BaseResponse


class ExtractedDependentDTO(BaseModel):
    id: Optional[int] = None
    extracted_application_id: Optional[int] = None
    dependant_id: Optional[int] = None
    full_name: Optional[str] = None
    full_name_confidence: Optional[float] = None
    id_number: Optional[str] = None
    id_number_confidence: Optional[float] = None
    date_of_birth: Optional[date] = None
    date_of_birth_confidence: Optional[float] = None
    age: Optional[int] = None
    age_confidence: Optional[float] = None
    gender: Optional[str] = None
    gender_confidence: Optional[float] = None
    client_relationship: Optional[str] = None
    client_relationship_confidence: Optional[float] = None

    entity_status: Optional[str] = None
    date_created: Optional[datetime] = None
    date_updated: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


class ExtractedDependentCreateRequest(BaseModel):
    extracted_application_id: Optional[int] = None
    dependant_id: Optional[int] = None
    full_name: Optional[str] = None
    full_name_confidence: Optional[float] = None
    id_number: Optional[str] = None
    id_number_confidence: Optional[float] = None
    date_of_birth: Optional[date] = None
    date_of_birth_confidence: Optional[float] = None
    age: Optional[int] = None
    age_confidence: Optional[float] = None
    gender: Optional[str] = None
    gender_confidence: Optional[float] = None
    client_relationship: Optional[str] = None
    client_relationship_confidence: Optional[float] = None
    model_config = ConfigDict(from_attributes=True)


class ExtractedDependentUpdateRequest(BaseModel):
    extracted_application_id: Optional[int] = None
    dependant_id: Optional[int] = None
    full_name: Optional[str] = None
    full_name_confidence: Optional[float] = None
    id_number: Optional[str] = None
    id_number_confidence: Optional[float] = None
    date_of_birth: Optional[date] = None
    date_of_birth_confidence: Optional[float] = None
    age: Optional[int] = None
    age_confidence: Optional[float] = None
    gender: Optional[str] = None
    gender_confidence: Optional[float] = None
    client_relationship: Optional[str] = None
    client_relationship_confidence: Optional[float] = None
    entity_status: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class ExtractedDependentResponse(BaseResponse):
    extracted_dependent: Optional[ExtractedDependentDTO] = None
    extracted_dependents: Optional[List[ExtractedDependentDTO]] = None
    model_config = ConfigDict(from_attributes=True)