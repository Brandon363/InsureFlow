from typing import Annotated
from fastapi import APIRouter
from fastapi.params import Depends
from requests import Session
from Config.database import get_db
from Model.ApplicationTrackingModel import ApplicationTrackingResponse, ApplicationTrackingCreateRequest, ApplicationTrackingUpdateRequest
from Service import ApplicationTrackingService

router = APIRouter(
    prefix="/application-tracking"
)

db_dependency = Annotated[Session, Depends(get_db)]


@router.get('/get-application-tracking-by-id/{application_tracking_id}', response_model=ApplicationTrackingResponse)
def get_application_tracking_by_id(application_tracking_id: int, db: db_dependency):
    return ApplicationTrackingService.get_application_tracking_by_id(db_session=db, application_tracking_id=application_tracking_id)


@router.get('/get-application-trackings-by-application-id/{application_id}', response_model=ApplicationTrackingResponse)
def get_application_trackings_by_application_id(application_id: int, db: db_dependency):
    return ApplicationTrackingService.get_application_trackings_by_application_id(db_session=db, application_id=application_id)


@router.post('/create-application-tracking', response_model=ApplicationTrackingResponse)
def create_application_tracking(create_request: ApplicationTrackingCreateRequest, db: db_dependency):
    return ApplicationTrackingService.create_application_tracking(db_session=db, create_request=create_request)


@router.put('/update-application-tracking/{application_tracking_id}', response_model=ApplicationTrackingResponse)
def update_application_tracking(application_tracking_id: int, update_request: ApplicationTrackingUpdateRequest, db: db_dependency):
    return ApplicationTrackingService.update_application_tracking(db_session=db, application_tracking_id=application_tracking_id, update_request=update_request)


@router.delete('/delete-application-tracking/{application_tracking_id}', response_model=ApplicationTrackingResponse)
def delete_application_tracking(application_tracking_id: int, db: db_dependency):
    return ApplicationTrackingService.delete_application_tracking(db_session=db, application_tracking_id=application_tracking_id)