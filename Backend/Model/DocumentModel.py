from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, List

from Model.ResponseModel import BaseResponse
from Utils.Enums import EntityStatus, DocumentType


class DocumentDTO(BaseModel):
    id: int
    user_id: int
    claim_id: Optional[int] = None
    policy_id: Optional[int] = None
    temporary_loss_application_id: Optional[int] = None
    type: DocumentType
    name: str
    url: str
    mime_type: str
    size: int
    date_created: datetime
    date_updated: Optional[datetime] = None
    entity_status: EntityStatus

    model_config = ConfigDict(from_attributes=True)


class DocumentCreate(BaseModel):
    user_id: int = Field(..., gt=0, description="Must be a valid user ID")
    claim_id: Optional[int] = Field(None, gt=0, description="Must be a valid claim ID if provided")
    policy_id: Optional[int] = Field(None, gt=0, description="Must be a valid policy ID if provided")
    temporary_loss_application_id: Optional[int] = Field(None, gt=0, description="Must be a valid policy ID if provided")
    type: DocumentType
    name: str = Field(..., min_length=1, max_length=100)
    url: str = Field(..., min_length=1, max_length=255)
    mime_type: str = Field(..., min_length=1, max_length=50)
    size: int = Field(..., gt=0)

    model_config = ConfigDict(from_attributes=True)


class DocumentUpdate(BaseModel):
    user_id: Optional[int] = None
    claim_id: Optional[int] = None
    policy_id: Optional[int] = None
    temporary_loss_application_id: Optional[int] = None
    type: Optional[DocumentType] = None
    name: Optional[str] = None
    url: Optional[str] = None
    mime_type: Optional[str] = None
    size: Optional[int] = None


class DocumentResponse(BaseResponse):
    document: Optional[DocumentDTO] = None
    documents: Optional[List[DocumentDTO]] = None

    model_config = ConfigDict(from_attributes=True)