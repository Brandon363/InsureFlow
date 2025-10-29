from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from Model.ResponseModel import BaseResponse
from Utils.Enums import ApplicationStage, TrackingStatus


class ApplicationTrackingDTO(BaseModel):
    id: int
    application_id: int
    stage: ApplicationStage
    status: TrackingStatus
    date_created: datetime
    user_id: int
    action_performed_by_id: int
    notes: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class ApplicationTrackingCreateRequest(BaseModel):
    application_id: int
    stage: ApplicationStage
    status: TrackingStatus
    user_id: int
    action_performed_by_id: int
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ApplicationTrackingUpdateRequest(BaseModel):
    id: int
    application_id: Optional[int]
    stage: Optional[ApplicationStage]
    status: Optional[TrackingStatus]
    user_id: Optional[int]
    action_performed_by_id: Optional[int]
    notes: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class ApplicationTrackingResponse(BaseResponse):
    application_tracking: Optional[ApplicationTrackingDTO] = None
    application_trackings: Optional[List[ApplicationTrackingDTO]] = None