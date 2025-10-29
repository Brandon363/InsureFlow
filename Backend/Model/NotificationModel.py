from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from Utils.Enums import NotificationType, EntityStatus, NotificationStatus


class NotificationDTO(BaseModel):
    id: int
    user_id: int
    claim_id: Optional[int] = None
    notification_type: NotificationType
    path_id: Optional[str] = None
    title: str
    message: str
    status: NotificationStatus
    related_id: Optional[int] = None
    is_read: bool
    read_at: Optional[datetime] = None
    date_created: datetime
    date_updated: Optional[datetime] = None
    entity_status: EntityStatus

    model_config = ConfigDict(from_attributes=True)


class NotificationCreate(BaseModel):
    user_id: int
    claim_id: Optional[int] = None
    notification_type: NotificationType
    path_id: Optional[str] = None
    title: str
    message: str
    related_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)


class NotificationUpdate(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    type: Optional[NotificationType] = None
    path_id: Optional[str] = None
    title: Optional[str] = None
    message: Optional[str] = None
    related_id: Optional[int] = None
    is_read: Optional[bool] = None
    model_config = ConfigDict(from_attributes=True)


# class NotificationResponse(BaseResponse):
#     notification: Optional[NotificationDTO] = None
#     notifications: Optional[List[NotificationDTO]] = None
#
#     model_config = ConfigDict(from_attributes=True)