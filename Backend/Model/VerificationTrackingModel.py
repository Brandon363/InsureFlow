from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from Model.ResponseModel import BaseResponse
from Utils.Enums import VerificationTrackingStage, TrackingStatus


class VerificationTrackingDTO(BaseModel):
    id: int
    stage: VerificationTrackingStage
    status: TrackingStatus
    date_created: datetime
    user_id: int
    action_performed_by_id: Optional[int]
    notes: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class VerificationTrackingCreateRequest(BaseModel):
    stage: VerificationTrackingStage
    status: TrackingStatus
    user_id: int
    action_performed_by_id: Optional[int] = None
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class VerificationTrackingUpdateRequest(BaseModel):
    id: int
    stage: Optional[VerificationTrackingStage]
    status: Optional[TrackingStatus]
    user_id: Optional[int]
    action_performed_by_id: Optional[int]
    notes: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class VerificationTrackingResponse(BaseResponse):
    verification_tracking: Optional[VerificationTrackingDTO] = None
    verification_trackings: Optional[List[VerificationTrackingDTO]] = None