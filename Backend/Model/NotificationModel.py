from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel

from Model.ResponseModel import BaseResponse
from Utils.Enums import NotificationType, EntityStatus


class NotificationDTO(BaseModel):
    id: int
    user_id: int
    type: NotificationType
    title: str
    message: str
    related_id: Optional[int] = None
    read: bool
    date_created: datetime
    date_updated: Optional[datetime] = None
    entity_status: EntityStatus

    class Config:
        from_attributes = True


class NotificationCreate(BaseModel):
    user_id: int
    type: NotificationType
    title: str
    message: str
    related_id: Optional[int] = None


class NotificationUpdate(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    type: Optional[NotificationType] = None
    title: Optional[str] = None
    message: Optional[str] = None
    related_id: Optional[int] = None
    read: Optional[bool] = None


class NotificationResponse(BaseResponse):
    notification: Optional[NotificationDTO] = None
    notifications: Optional[List[NotificationDTO]] = None

    class Config:
        from_attributes = True