from sqlalchemy.orm import Session
from Model.NotificationModel import NotificationCreate, NotificationUpdate, \
    NotificationDTO
from Entity.NotificationEntity import NotificationEntity
from Model.ResponseModel import BaseResponse
from Repository import notification_repository, user_repository
from Utils.Enums import EntityStatus
from datetime import datetime


def get_active_notification_by_id(db_session: Session, notification_id: int) -> BaseResponse:
    if notification_id is None:
        return BaseResponse(status_code=400, success=False, message="Notification ID cannot be null")
    db_notification = notification_repository.find_active_notification_by_id(db_session=db_session, notification_id=notification_id)
    if db_notification is None:
        return BaseResponse(status_code=404, success=False, message=f"Notification with id {notification_id} not found")

    return BaseResponse(status_code=200, success=True, message="Notification successfully found", notification=db_notification)


def get_active_notification_by_claim_id(db_session: Session, claim_id: int) -> BaseResponse:
    if claim_id is None:
        return BaseResponse(status_code=400, success=False, message="Claim ID cannot be null")
    db_notification = notification_repository.find_active_notification_by_claim_id(db_session=db_session, claim_id=claim_id)
    if db_notification is None:
        return BaseResponse(status_code=404, success=False, message=f"Notification with claim ID {claim_id} not found")

    return BaseResponse(status_code=200, success=True, message="Notification successfully found", notification=db_notification)


def get_active_notifications_by_user_id(db_session: Session, user_id: int) -> BaseResponse:
    if user_id is None:
        return BaseResponse(status_code=400, success=False, message="User ID cannot be null")
    db_user_id = notification_repository.find_active_notifications_by_user_id(db_session=db_session, user_id=user_id)
    if db_user_id is None:
        return BaseResponse(status_code=404, success=False, message=f"Notifications for user ID {user_id} not found")

    return BaseResponse(status_code=200, success=True, message="Notifications successfully found", notifications=db_user_id)


def get_unread_notifications_by_user_id(db_session: Session, user_id: int) -> BaseResponse:
    if user_id is None:
        return BaseResponse(status_code=400, success=False, message="User ID cannot be null")
    db_user_id = notification_repository.find_unread_notifications_by_user_id(db_session=db_session, user_id=user_id)
    if db_user_id is None:
        return BaseResponse(status_code=404, success=False, message=f"Unread notifications for user ID {user_id} not found")

    return BaseResponse(status_code=200, success=True, message="Unread notifications successfully found", notifications=db_user_id)


def get_all_active_notifications(db_session: Session) -> BaseResponse:
    db_notifications = notification_repository.find_all_active_notifications(db_session=db_session)
    if db_notifications is None:
        return BaseResponse(status_code=404, success=False, message="Notifications not found")

    return BaseResponse(status_code=200, success=True, message="Notifications successfully found", notifications=db_notifications)


def create_notification(db_session: Session, create_request: NotificationCreate) -> BaseResponse:
    existing_user = user_repository.find_active_user_by_id(db_session=db_session, user_id=create_request.user_id)

    if not existing_user:
        return BaseResponse(status_code=404, success=False, message=f"User ID {create_request.user_id} not found")

    db_notification_response = get_active_notification_by_claim_id(db_session=db_session,
                                                         claim_id=create_request.claim_id)

    if db_notification_response.success:
        return BaseResponse(status_code=400, success=False, message="Notification ID already exists")

    notification_entity: NotificationEntity = NotificationEntity(**create_request.dict())
    db_session.add(notification_entity)
    db_session.commit()
    db_session.refresh(notification_entity)

    return BaseResponse(status_code=200, success=True, message="Notification created successfully", notification=notification_entity)


def update_notification(db_session: Session, notification_id: int, update_request: NotificationUpdate) -> BaseResponse:
    existing_notification = notification_repository.find_active_notification_by_id(db_session=db_session, notification_id=notification_id)

    if not existing_notification:
        return BaseResponse(status_code=404, success=False, message=f"Notification with ID {notification_id} not found")

    if update_request.id != existing_notification.notification_id:
        notification_with_the_same_id = notification_repository.find_active_notification_by_id(db_session=db_session,
                                                                                        notification_id=update_request.id)

        if notification_with_the_same_id:
            return BaseResponse(status_code=400, success=False,
                                 message=f"Notification ID '{update_request.id}' already exists")

    update_dict = update_request.dict(exclude_unset=True)

    for key, value in update_dict.items():
        if value is not None and hasattr(existing_notification, key):
            setattr(existing_notification, key, value)

    db_session.commit()
    db_session.refresh(existing_notification)
    return BaseResponse(status_code=200, success=True, message="Notification edited successfully", notification=existing_notification)


def delete_notification(db_session: Session, notification_id: int) -> BaseResponse:
    existing_notification = notification_repository.find_active_notification_by_id(db_session=db_session, notification_id=notification_id)

    if existing_notification is None:
        return BaseResponse(status_code=404, success=False, message=f"Notification with ID {notification_id} does not exist")

    existing_notification.entity_status = EntityStatus.DELETED
    db_session.delete(existing_notification)
    db_session.commit()

    return BaseResponse(status_code=201, message="Notification successfully deleted", success=True, notification=existing_notification)