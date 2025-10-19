from fastapi import APIRouter
from fastapi.params import Depends
from requests import Session
from typing import Annotated

from Config.database import get_db
from Model.ClaimModel import ClaimCreate, ClaimUpdate, ClaimResponse
from Service import ClaimService

router = APIRouter(
    prefix="/claim",
)


db_dependency = Annotated[Session, Depends(get_db)]


@router.get('/get-active-claim-by-id{claim_id}', response_model=ClaimResponse)
def get_active_claim_by_id(claim_id: int, db: db_dependency):
    return ClaimService.get_active_claim_by_id(db_session=db, claim_id=claim_id)


@router.get('/get-active-user-by-claim-number{claim_number}', response_model=ClaimResponse)
def get_active_claim_by_claim_number(claim_number: str, db: db_dependency):
    return ClaimService.get_active_claim_by_claim_number(db_session=db, claim_number=claim_number)


@router.get('/get-active-user-by-policy-id{policy_id}', response_model=ClaimResponse)
def get_active_claim_by_policy_id(policy_id: int, db: db_dependency):
    return ClaimService.get_active_claim_by_policy_id(db_session=db, policy_id=policy_id)


@router.get('/get-active-by-user-id{user_id}', response_model=ClaimResponse)
def get_active_claim_by_user_id(user_id: int, db: db_dependency):
    return ClaimService.get_active_claim_by_user_id(db_session=db, user_id=user_id)


@router.get('/get-all-active-claims', response_model=ClaimResponse)
def get_all_active_claims(db: db_dependency):
    return ClaimService.get_all_active_claims(db_session=db)


@router.post('/create-claim', response_model=ClaimResponse)
def create_claim (create_request: ClaimCreate, db: db_dependency):
    return ClaimService.create_claim(db_session=db, create_request=create_request)


@router.put('update-claim/{claim_id}', response_model=ClaimResponse)
def update_user (update_request: ClaimUpdate, claim_id: int, db: db_dependency):
    update_request.id = claim_id
    return ClaimService.update_claim(db_session=db, claim_id=claim_id, update_request=update_request)


@router.delete('delete-claim/{claim_id}', response_model=ClaimResponse)
def delete_user (claim_id: int, db: db_dependency) -> ClaimResponse:
    return ClaimService.delete_claim(db_session=db, claim_id=claim_id)
