from typing import Annotated
from fastapi import APIRouter
from fastapi.params import Depends
from requests import Session
from Config.database import get_db
from Model.TemporaryLossApplicationModel import TemporaryLossApplicationResponse, TemporaryLossApplicationCreateRequest, TemporaryLossApplicationUpdateRequest
from Service import TemporaryLossApplicationService

router = APIRouter(
    prefix="/temporary_loss_application"
)

db_dependency = Annotated[Session, Depends(get_db)]


@router.get('/get-temporary-loss-application-by-id/{application_id}', response_model=TemporaryLossApplicationResponse)
def get_temporary_loss_application_by_id(application_id: int, db: db_dependency):
    return TemporaryLossApplicationService.get_temporary_loss_application_by_id(db_session=db, application_id=application_id)


@router.get('/get-all-temporary-loss-applications', response_model=TemporaryLossApplicationResponse)
def get_all_temporary_loss_applications(db: db_dependency):
    return TemporaryLossApplicationService.get_all_temporary_loss_applications(db_session=db)


@router.get('/get-all-user-temporary-loss-applications/{id_number}', response_model=TemporaryLossApplicationResponse)
def get_all_temporary_loss_applications(db: db_dependency, id_number:str):
    return TemporaryLossApplicationService.get_all_user_temporary_loss_applications(db_session=db, id_number= id_number)


@router.post('/create-temporary-loss-application', response_model=TemporaryLossApplicationResponse)
def create_temporary_loss_application(create_request: TemporaryLossApplicationCreateRequest, db: db_dependency):
    return TemporaryLossApplicationService.create_temporary_loss_application(db_session=db, create_request=create_request)


@router.put('/update-temporary-loss-application/{application_id}', response_model=TemporaryLossApplicationResponse)
def update_temporary_loss_application(application_id: int, update_request: TemporaryLossApplicationUpdateRequest, db: db_dependency):
    return TemporaryLossApplicationService.update_temporary_loss_application(db_session=db, application_id=application_id, update_request=update_request)


@router.put('/update-temporary-loss-application-and-dependents/{application_id}', response_model=TemporaryLossApplicationResponse)
def update_temporary_loss_application_and_dependents(application_id: int, update_request: TemporaryLossApplicationUpdateRequest, db: db_dependency):
    return TemporaryLossApplicationService.update_temporary_loss_application_and_dependents(db_session=db, application_id=application_id, update_request=update_request)


@router.put('/verify-documents/{application_id}/{verifier_id}', response_model=TemporaryLossApplicationResponse)
def update_temporary_loss_application_and_dependents(verifier_id: int, application_id: int, db: db_dependency):
    return TemporaryLossApplicationService.verifyDocuments(db_session=db, application_id=application_id, verifier_id=verifier_id)



@router.delete('/delete-temporary-loss-application/{application_id}', response_model=TemporaryLossApplicationResponse)
def delete_temporary_loss_application(application_id: int, db: db_dependency):
    return TemporaryLossApplicationService.delete_temporary_loss_application(db_session=db, application_id=application_id)