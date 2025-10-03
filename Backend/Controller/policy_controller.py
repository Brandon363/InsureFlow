from typing import Annotated
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from Config.database import get_db
from Model.PolicyModel import PolicyResponse, PolicyCreateRequest, PolicyUpdateRequest
from Service import PolicyService

router = APIRouter(
    prefix="/policy"
)


db_dependency = Annotated[Session, Depends(get_db)]


@router.get('/get-active-policy-by-id/{policy_id}', response_model=PolicyResponse)
def get_active_policy_by_id(policy_id: int, db: db_dependency):
    return PolicyService.get_active_policy_by_id(db_session=db, policy_id=policy_id)


@router.get('/get-active-policy-by-policy-number/{policy_number}', response_model=PolicyResponse)
def get_active_policy_by__policy_number(policy_number: str, db: db_dependency):
    return PolicyService.get_active_policy_by_policy_number(db_session=db, policy_number=policy_number)


@router.get('/get-active-policy-by-user-id/{user_id}', response_model=PolicyResponse)
def get_active_policy_by_user_id(user_id: int, db: db_dependency):
    return PolicyService.get_active_policy_by_user_id(db_session=db, user_id=user_id)


@router.get('/get-all-active-policies', response_model=PolicyResponse)
def get_all_active_policies(db: db_dependency):
    return PolicyService.get_all_active_policies(db_session=db)


@router.post('/create-policy', response_model=PolicyResponse)
def create_policy(create_request: PolicyCreateRequest, db: db_dependency):
    return PolicyService.create_policy(db_session=db, create_request=create_request)


@router.put('update-policy/{policy_id}', response_model=PolicyResponse)
def update_policy(update_request: PolicyUpdateRequest, policy_id: int, db: db_dependency):
    return PolicyService.update_policy(db_session=db, update_request=update_request)


@router.delete('delete-policy/{policy_id}', response_model=PolicyResponse)
def delete_policy(policy_id: int, db: db_dependency) -> PolicyResponse:
    return PolicyService.delete_policy(db_session=db,policy_id=policy_id)