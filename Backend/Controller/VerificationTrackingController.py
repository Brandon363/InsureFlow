from typing import Annotated
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from Config.database import get_db
from Model.VerificationTrackingModel import VerificationTrackingResponse, VerificationTrackingCreateRequest, VerificationTrackingUpdateRequest
from Service import VerificationTrackingService

router = APIRouter(
    prefix="/verification-tracking"
)

db_dependency = Annotated[Session, Depends(get_db)]


@router.get('/get-verification-tracking-by-id/{verification_tracking_id}', response_model=VerificationTrackingResponse)
def get_verification_tracking_by_id(verification_tracking_id: int, db: db_dependency):
    return VerificationTrackingService.get_verification_tracking_by_id(db_session=db, verification_tracking_id=verification_tracking_id)


@router.get('/get-verification-trackings-by-user-id/{user_id}', response_model=VerificationTrackingResponse)
def get_verification_trackings_by_user_id(user_id: int, db: db_dependency):
    return VerificationTrackingService.get_verification_trackings_by_user_id(db_session=db, user_id=user_id)


@router.post('/create-verification-tracking', response_model=VerificationTrackingResponse)
def create_verification_tracking(create_request: VerificationTrackingCreateRequest, db: db_dependency):
    return VerificationTrackingService.create_verification_tracking(db_session=db, create_request=create_request)


@router.put('/update-verification-tracking/{verification_tracking_id}', response_model=VerificationTrackingResponse)
def update_verification_tracking(verification_tracking_id: int, update_request: VerificationTrackingUpdateRequest, db: db_dependency):
    return VerificationTrackingService.update_verification_tracking(db_session=db, verification_tracking_id=verification_tracking_id, update_request=update_request)


@router.delete('/delete-verification-tracking/{verification_tracking_id}', response_model=VerificationTrackingResponse)
def delete_verification_tracking(verification_tracking_id: int, db: db_dependency):
    return VerificationTrackingService.delete_verification_tracking(db_session=db, verification_tracking_id=verification_tracking_id)