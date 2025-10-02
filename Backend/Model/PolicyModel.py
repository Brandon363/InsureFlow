from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List

from Model.ResponseModel import BaseResponse
from Utils.Enums import PolicyType, PolicyStatus, EntityStatus

class PolicyDTO(BaseModel):
    id: int
    policy_number: str
    user_id: int
    type: PolicyType
    status: PolicyStatus
    start_date: date
    end_date: date
    premium: float
    coverage: float
    deductible: float
    details: dict
    date_created: datetime
    date_updated: Optional[datetime] = None
    entity_status: EntityStatus

    class Config:
        from_attributes = True

class PolicyCreateRequest(BaseModel):
    policy_number: str
    user_id: int
    type: PolicyType
    status: PolicyStatus
    start_date: date
    end_date: date
    premium: float
    coverage: float
    deductible: float
    details: dict

class PolicyUpdateRequest(BaseModel):
    policy_number: int
    policy_number: Optional[str] = None
    user_id: Optional[int] = None
    type: Optional[PolicyType] = None
    status: Optional[PolicyStatus] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    premium: Optional[float] = None
    coverage: Optional[float] = None
    deductible: Optional[float] = None
    details: Optional[dict] = None
    entity_status: Optional[EntityStatus] = None

class PolicyResponse(BaseResponse):
    policy: Optional[PolicyDTO] = None
    policies: Optional[List[PolicyDTO]] = None

    class Config:
        from_attributes = True