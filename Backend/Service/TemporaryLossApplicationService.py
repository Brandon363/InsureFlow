from sqlalchemy.orm import Session
from Entity.TemporaryLossApplicationEntity import TemporaryLossApplicationEntity
from Model.ApplicationTrackingModel import ApplicationTrackingUpdateRequest, ApplicationTrackingCreateRequest
from Model.TemporaryLossApplicationModel import TemporaryLossApplicationResponse, TemporaryLossApplicationCreateRequest, TemporaryLossApplicationUpdateRequest
from Repository import TemporaryLossApplicationRepository
from Utils.Enums import EntityStatus, ApplicationStage, TrackingStatus
from Service.DependentService import update_multiple_dependents
from Service.ApplicationTrackingService import create_application_tracking

def get_temporary_loss_application_by_id(db_session: Session, application_id: int) -> TemporaryLossApplicationResponse:
    if application_id is None:
        return TemporaryLossApplicationResponse(status_code=400, success=False, message="Application ID cannot be null")

    db_application = TemporaryLossApplicationRepository.find_temporary_loss_application_by_id(db_session=db_session, application_id=application_id)

    if db_application is None:
        return TemporaryLossApplicationResponse(status_code=404, success=False, message=f"Application with id {application_id} not found")

    return TemporaryLossApplicationResponse(status_code=200, success=True, message="Application successfully found", temporary_loss_application=db_application)


def get_all_temporary_loss_applications(db_session: Session) -> TemporaryLossApplicationResponse:
    db_applications = TemporaryLossApplicationRepository.find_all_temporary_loss_applications(db_session=db_session)

    if db_applications is None:
        return TemporaryLossApplicationResponse(status_code=404, success=False, message="Applications not found")

    return TemporaryLossApplicationResponse(status_code=200, success=True, message="Applications successfully found", temporary_loss_applications=db_applications)



def get_all_user_temporary_loss_applications(db_session: Session, id_number: str) -> TemporaryLossApplicationResponse:
    db_applications = TemporaryLossApplicationRepository.find_all_user_temporary_loss_applications(db_session=db_session, id_number=id_number)

    if db_applications is None:
        return TemporaryLossApplicationResponse(status_code=404, success=False, message="Applications not found")

    return TemporaryLossApplicationResponse(status_code=200, success=True, message="Applications successfully found", temporary_loss_applications=db_applications)


def create_temporary_loss_application(db_session: Session, create_request: TemporaryLossApplicationCreateRequest) -> TemporaryLossApplicationResponse:
    application_entity = TemporaryLossApplicationEntity()

    for key, value in create_request.dict().items():
        if hasattr(application_entity, key):
            setattr(application_entity, key, value)

    db_session.add(application_entity)
    db_session.commit()
    db_session.refresh(application_entity)

    return TemporaryLossApplicationResponse(status_code=201, success=True, message="Application created successfully", temporary_loss_application=application_entity)


def update_temporary_loss_application(db_session: Session, application_id: int, update_request: TemporaryLossApplicationUpdateRequest) -> TemporaryLossApplicationResponse:
    db_application = TemporaryLossApplicationRepository.find_temporary_loss_application_by_id(db_session=db_session, application_id=application_id)

    if not db_application:
        return TemporaryLossApplicationResponse(status_code=404, success=False, message=f"Application with id {application_id} not found")

    # update_dict = update_request.dict(exclude_unset=True)
    update_dict = update_request.dict(exclude={"dependents"}, exclude_unset=True)

    for key, value in update_dict.items():
        if value is not None and hasattr(db_application, key):
            setattr(db_application, key, value)

    db_session.commit()
    db_session.refresh(db_application)
    return TemporaryLossApplicationResponse(status_code=200, success=True, message="Application successfully updated", temporary_loss_application=db_application)


def delete_temporary_loss_application(db_session: Session, application_id: int) -> TemporaryLossApplicationResponse:
    existing_application = TemporaryLossApplicationRepository.find_temporary_loss_application_by_id(db_session=db_session, application_id=application_id)

    if existing_application is None:
        return TemporaryLossApplicationResponse(status_code=404, success=False, message="Application does not exist")

    existing_application.entity_status = EntityStatus.DELETED
    db_session.commit()

    return TemporaryLossApplicationResponse(status_code=201, success=True, message="Application successfully deleted", temporary_loss_application=existing_application)


def update_temporary_loss_application_and_dependents(
    db_session: Session, application_id: int, update_request: TemporaryLossApplicationUpdateRequest):

    update_application_response = update_temporary_loss_application(
        db_session=db_session, application_id=application_id, update_request=update_request
    )

    if not update_application_response.success:
        return TemporaryLossApplicationResponse(
            status_code=update_application_response.status_code, success=False,
            message=update_application_response.message)

    dependent_update_requests = update_request.dependents
    update_dependents_response = update_multiple_dependents(
        db_session=db_session, update_requests=dependent_update_requests
    )

    if not update_dependents_response.success:
        return TemporaryLossApplicationResponse(
            status_code=update_dependents_response.status_code,
            success=False,
            message=update_dependents_response.message)

    return TemporaryLossApplicationResponse(status_code=200, success=True,
                                            message="Application successfully updated",
                                            temporary_loss_application=update_application_response.temporary_loss_application)


def verifyDocuments(db_session: Session, application_id: int, verifier_id: int):
    application_response = get_temporary_loss_application_by_id(db_session=db_session, application_id=application_id)

    if not application_response.success:
        return TemporaryLossApplicationResponse(
            status_code=application_response.status_code,
            success=False,
            message=application_response.message)

    tracking_request = ApplicationTrackingCreateRequest(
        application_id=application_id,
        stage=ApplicationStage.DOCUMENTS_VERIFIED,
        status=TrackingStatus.PENDING,
        action_performed_by_id=verifier_id
        )
    create_response = create_application_tracking(db_session=db_session, create_request=tracking_request)
    if not create_response.success:
        return TemporaryLossApplicationResponse(
            status_code=create_response.status_code,
            success=False,
            message=create_response.message)
    application_response.temporary_loss_application.application_tracking_stages.append(
        create_response.application_tracking
    )
    return TemporaryLossApplicationResponse(
        status_code=201, success=True, message="Documents Verified",
        temporary_loss_application= application_response.temporary_loss_application)
