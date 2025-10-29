from typing import Annotated
from fastapi import APIRouter
from fastapi.params import Depends
from requests import Session
from Config.database import get_db
from Model.DependentModel import DependentResponse, DependentCreateRequest, DependentUpdateRequest
from Service import DependentService

router = APIRouter(
    prefix="/dependent"
)

db_dependency = Annotated[Session, Depends(get_db)]


@router.get('/get-dependent-by-id/{dependent_id}', response_model=DependentResponse)
def get_dependent_by_id(dependent_id: int, db: db_dependency):
    return DependentService.get_dependent_by_id(db_session=db, dependent_id=dependent_id)


@router.get('/get-dependents-by-application-id/{application_id}', response_model=DependentResponse)
def get_dependents_by_application_id(application_id: int, db: db_dependency):
    return DependentService.get_dependents_by_application_id(db_session=db, application_id=application_id)


@router.post('/create-dependent', response_model=DependentResponse)
def create_dependent(create_request: DependentCreateRequest, db: db_dependency):
    return DependentService.create_dependent(db_session=db, create_request=create_request)


@router.put('/update-dependent/{dependent_id}', response_model=DependentResponse)
def update_dependent(dependent_id: int, update_request: DependentUpdateRequest, db: db_dependency):
    return DependentService.update_dependent(db_session=db, dependent_id=dependent_id, update_request=update_request)


@router.delete('/delete-dependent/{dependent_id}', response_model=DependentResponse)
def delete_dependent(dependent_id: int, db: db_dependency):
    return DependentService.delete_dependent(db_session=db, dependent_id=dependent_id)