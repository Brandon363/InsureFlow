from sqlalchemy.orm import Session

from Entity.VerificationTrackingEntity import VerificationTrackingEntity
from Model.VerificationTrackingModel import VerificationTrackingResponse, VerificationTrackingCreateRequest, \
    VerificationTrackingUpdateRequest
from Repository import VerificationTrackingRepository
from Utils.Enums import EntityStatus


def get_verification_tracking_by_id(db_session: Session, verification_tracking_id: int) -> VerificationTrackingResponse:
    if verification_tracking_id is None:
        return VerificationTrackingResponse(status_code=400, success=False,
                                           message="Verification tracking ID cannot be null")

    db_verification_tracking = VerificationTrackingRepository.find_verification_tracking_by_id(db_session=db_session,
                                                                                              verification_tracking_id=verification_tracking_id)

    if db_verification_tracking is None:
        return VerificationTrackingResponse(status_code=404, success=False,
                                           message=f"Verification tracking with id {verification_tracking_id} not found")

    return VerificationTrackingResponse(status_code=200, success=True, message="Verification tracking successfully found",
                                       verification_tracking=db_verification_tracking)


def get_verification_trackings_by_user_id(db_session: Session, user_id: int) -> VerificationTrackingResponse:
    if user_id is None:
        return VerificationTrackingResponse(status_code=400, success=False, message="User ID cannot be null")

    db_verification_trackings = VerificationTrackingRepository.find_verification_trackings_by_user_id(
        db_session=db_session, user_id=user_id)

    if not db_verification_trackings:
        return VerificationTrackingResponse(status_code=404, success=False,
                                           message=f"Verification trackings for user {user_id} not found")

    return VerificationTrackingResponse(status_code=200, success=True,
                                       message="Verification trackings successfully found",
                                       verification_trackings=db_verification_trackings)


def create_verification_tracking(db_session: Session,
                                create_request: VerificationTrackingCreateRequest) -> VerificationTrackingResponse:
    verification_tracking_entity = VerificationTrackingEntity()

    for key, value in create_request.dict().items():
        if hasattr(verification_tracking_entity, key):
            setattr(verification_tracking_entity, key, value)

    db_session.add(verification_tracking_entity)
    db_session.commit()
    db_session.refresh(verification_tracking_entity)

    return VerificationTrackingResponse(status_code=201, success=True,
                                       message="Verification tracking created successfully",
                                       verification_tracking=verification_tracking_entity)


def update_verification_tracking(db_session: Session, verification_tracking_id: int,
                                update_request: VerificationTrackingUpdateRequest) -> VerificationTrackingResponse:
    db_verification_tracking = VerificationTrackingRepository.find_verification_tracking_by_id(db_session=db_session,
                                                                                              verification_tracking_id=verification_tracking_id)

    if not db_verification_tracking:
        return VerificationTrackingResponse(status_code=404, success=False,
                                           message=f"Verification tracking with id {verification_tracking_id} not found")

    update_dict = update_request.dict(exclude_unset=True)

    for key, value in update_dict.items():
        if value is not None and hasattr(db_verification_tracking, key):
            setattr(db_verification_tracking, key, value)

    db_session.commit()
    db_session.refresh(db_verification_tracking)
    return VerificationTrackingResponse(status_code=200, success=True,
                                       message="Verification tracking successfully updated",
                                       verification_tracking=db_verification_tracking)


def delete_verification_tracking(db_session: Session, verification_tracking_id: int) -> VerificationTrackingResponse:
    existing_verification_tracking = VerificationTrackingRepository.find_verification_tracking_by_id(
        db_session=db_session, verification_tracking_id=verification_tracking_id)

    if existing_verification_tracking is None:
        return VerificationTrackingResponse(status_code=404, success=False,
                                           message="Verification tracking does not exist")

    existing_verification_tracking.entity_status = EntityStatus.DELETED
    db_session.commit()

    return VerificationTrackingResponse(status_code=201, success=True,
                                       message="Verification tracking successfully deleted")