from pydantic import BaseModel
from typing import Optional, List

from Model.NotificationModel import NotificationDTO


class ErrorDetail(BaseModel):
    field: str
    message: str


class BaseResponse(BaseModel):
    status_code: int
    success: bool
    message: str
    errors: Optional[List[ErrorDetail]] | dict = None
    notification: Optional[NotificationDTO] = None
    notifications: Optional[List[NotificationDTO]] = None
