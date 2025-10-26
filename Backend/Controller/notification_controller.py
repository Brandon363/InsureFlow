from typing import Annotated
from fastapi import APIRouter
from requests import Session

from fastapi.params import Depends
from Config.database import get_db
from Model.NotificationModel import NotificationCreate, NotificationUpdate
from Model.ResponseModel import BaseResponse
from Service import NotificationService

router = APIRouter(
    prefix="/notification"
)

db_dependency = Annotated[Session, Depends(get_db)]


@router.get('/get-active-notification-by-id/{notification_id}', response_model=BaseResponse)
def get_active_notification_by_id(notification_id: int, db: db_dependency):
    return NotificationService.get_active_notification_by_id(db_session=db, notification_id=notification_id)


@router.get('/get-active-notification-by-claim-id/{claim_id}', response_model=BaseResponse)
def get_active_notification_by_claim_id(claim_id: int, db: db_dependency):
    return NotificationService.get_active_notification_by_claim_id(db_session=db, claim_id=claim_id)


@router.get('/get-active-notifications-by-user/{user_id}', response_model=BaseResponse)
def get_active_notifications_by_user_id(user_id: int, db: db_dependency):
    return NotificationService.get_active_notifications_by_user_id(db_session=db, user_id=user_id)


@router.get('/get-unread-notifications-by-user/{user_id}', response_model=BaseResponse)
def get_unread_notifications_by_user_id(user_id: int, db: db_dependency):
    return NotificationService.get_unread_notifications_by_user_id(db_session=db, user_id=user_id)


@router.get('/get-all-active-notifications', response_model=BaseResponse)
def get_all_active_notifications(db: db_dependency):
    return NotificationService.get_all_active_notifications(db_session=db)


@router.get('/get-all-active-notifications-by-user-id/{user_id}', response_model=BaseResponse)
def get_all_active_notifications(db: db_dependency, user_id: int):
    return NotificationService.get_all_active_notifications_by_user_id(db_session=db, user_id=user_id)


@router.post('/create-notification', response_model=BaseResponse)
def create_notification(create_request: NotificationCreate, db: db_dependency):
    return NotificationService.create_notification(db_session=db, create_request=create_request)


@router.put('/update-notification/{notification_id}', response_model=BaseResponse)
def update_notification(update_request: NotificationUpdate, notification_id: int, db: db_dependency):
    update_request.id = notification_id
    return NotificationService.update_notification(db_session=db, notification_id=notification_id, update_request=update_request)



@router.put('/mark-all-as-read/{user_id}', response_model=BaseResponse)
def update_notification(user_id: int, db: db_dependency):
    return NotificationService.mark_all_as_read(db_session=db, user_id=user_id)


@router.delete('/delete-notification/{notification_id}', response_model=BaseResponse)
def delete_notification(notification_id: int, db: db_dependency) -> BaseResponse:
    return NotificationService.delete_notification(db_session=db, notification_id=notification_id)
