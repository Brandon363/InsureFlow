from datetime import datetime
from sqlalchemy.orm import Session
from Entity.ApplicationTrackingEntity import ApplicationTrackingEntity
from Model.ApplicationTrackingModel import ApplicationTrackingResponse, ApplicationTrackingCreateRequest, \
    ApplicationTrackingUpdateRequest
from Repository import ApplicationTrackingRepository
from Utils.Enums import EntityStatus


def get_application_tracking_by_id(db_session: Session, application_tracking_id: int) -> ApplicationTrackingResponse:
    if application_tracking_id is None:
        return ApplicationTrackingResponse(status_code=400, success=False,
                                           message="Application tracking ID cannot be null")

    db_application_tracking = ApplicationTrackingRepository.find_application_tracking_by_id(db_session=db_session,
                                                                                              application_tracking_id=application_tracking_id)

    if db_application_tracking is None:
        return ApplicationTrackingResponse(status_code=404, success=False,
                                           message=f"Application tracking with id {application_tracking_id} not found")

    return ApplicationTrackingResponse(status_code=200, success=True, message="Application tracking successfully found",
                                       application_tracking=db_application_tracking)


def get_application_trackings_by_application_id(db_session: Session,
                                                application_id: int) -> ApplicationTrackingResponse:
    if application_id is None:
        return ApplicationTrackingResponse(status_code=400, success=False, message="Application ID cannot be null")

    db_application_trackings = ApplicationTrackingRepository.find_application_trackings_by_application_id(
        db_session=db_session, application_id=application_id)

    if db_application_trackings is None:
        return ApplicationTrackingResponse(status_code=404, success=False,
                                           message=f"Application trackings for application {application_id} not found")

    return ApplicationTrackingResponse(status_code=200, success=True,
                                       message="Application trackings successfully found",
                                       application_trackings=db_application_trackings)


def create_application_tracking(db_session: Session,
                                create_request: ApplicationTrackingCreateRequest) -> ApplicationTrackingResponse:
    application_tracking_entity = ApplicationTrackingEntity()

    for key, value in create_request.dict().items():
        if hasattr(application_tracking_entity, key):
            setattr(application_tracking_entity, key, value)

    db_session.add(application_tracking_entity)
    db_session.commit()
    db_session.refresh(application_tracking_entity)

    return ApplicationTrackingResponse(status_code=201, success=True,
                                       message="Application tracking created successfully",
                                       application_tracking=application_tracking_entity)


def update_application_tracking(db_session: Session, application_tracking_id: int,
                                update_request: ApplicationTrackingUpdateRequest) -> ApplicationTrackingResponse:
    db_application_tracking = ApplicationTrackingRepository.find_application_tracking_by_id(db_session=db_session,
                                                                                              application_tracking_id=application_tracking_id)

    if not db_application_tracking:
        return ApplicationTrackingResponse(status_code=404, success=False,
                                           message=f"Application tracking with id {application_tracking_id} not found")

    update_dict = update_request.dict(exclude_unset=True)

    for key, value in update_dict.items():
        if value is not None and hasattr(db_application_tracking, key):
            setattr(db_application_tracking, key, value)

    db_session.commit()
    db_session.refresh(db_application_tracking)
    return ApplicationTrackingResponse(status_code=200, success=True,
                                       message="Application tracking successfully updated",
                                       application_tracking=db_application_tracking)


def delete_application_tracking(db_session: Session, application_tracking_id: int) -> ApplicationTrackingResponse:
    existing_application_tracking = ApplicationTrackingRepository.find_application_tracking_by_id(
        db_session=db_session, application_tracking_id=application_tracking_id)

    if existing_application_tracking is None:
        return ApplicationTrackingResponse(status_code=404, success=False,
                                           message="Application tracking does not exist")

    existing_application_tracking.entity_status = EntityStatus.DELETED
    db_session.commit()

    return ApplicationTrackingResponse(status_code=201, success=True,
                                       message="Application tracking successfully deleted",
                                       application_tracking=existing_application_tracking)