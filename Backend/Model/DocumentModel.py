from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional, List

from Model.ResponseModel import BaseResponse
from Utils.Enums import EntityStatus


class DocumentDTO(BaseModel):
    id: int
    user_id: int
    claim_id: Optional[int] = None
    policy_id: Optional[int] = None
    type: str
    name: str
    url: str
    mime_type: str
    size: int
    date_created: datetime
    date_updated: Optional[datetime] = None
    entity_status: EntityStatus

    model_config = ConfigDict(from_attributes=True)


class DocumentCreate(BaseModel):
    user_id: int
    claim_id: Optional[int]
    policy_id: Optional[int]
    type: str
    name: str
    url: str
    mime_type: str
    size: int

class DocumentUpdate(BaseModel):
    id: int
    user_id: Optional[int] = None
    claim_id: Optional[int] = None
    policy_id: Optional[int] = None
    type: Optional[str] = None
    name: Optional[str] = None
    url: Optional[str] = None
    mime_type: Optional[str] = None
    size: Optional[int] = None

class DocumentResponse(BaseResponse):
    document: Optional[DocumentDTO] = None
    documents: Optional[List[DocumentDTO]] = None

    class Config:
        from_attributes = True