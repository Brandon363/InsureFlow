from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from Model.ResponseModel import BaseResponse
from Utils.Enums import ClaimStatus, EntityStatus


class ClaimDTO(BaseModel):
    id: int
    claim_number: str
    policy_id: int
    user_id: int
    type: str
    status: ClaimStatus
    description: str
    incident_date: date
    amount: float
    documents: List[str] = None
    notes: Optional[str] = None
    approved_amount: Optional[float]
    date_created: datetime
    date_updated: datetime
    entity_status: EntityStatus
    model_config = ConfigDict(from_attributes=True)


class ClaimCreate(BaseModel):
    pass


class ClaimUpdate(BaseModel):
    id: int
    claim_number: Optional[str]
    policy_id: Optional[str]
    user_id: Optional[int]
    type: Optional[str]
    status: Optional[ClaimStatus]
    description: Optional[str]
    incident_date: Optional[date]
    amount: Optional[float]
    documents: Optional[List[str]]
    notes: Optional[str]
    approved_amount: Optional[float]


class ClaimResponse(BaseResponse):
    claim: Optional[ClaimDTO] = None
    claims: Optional[List[ClaimDTO]] = None

    model_config = ConfigDict(from_attributes=True)