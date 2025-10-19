from sqlalchemy.orm import Session
from Model.ClaimModel import ClaimResponse, ClaimCreate, ClaimUpdate
from Entity.ClaimEntity import ClaimEntity
from Repository import claim_repository, user_repository
from Utils.Enums import EntityStatus


def get_active_claim_by_id(db_session: Session, claim_id: int) -> ClaimResponse:
    if claim_id is None:
        return ClaimResponse(status_code=400, success=False, message="Claim ID cannot be null")
    db_claim = claim_repository.find_active_claim_by_id(db_session=db_session, claim_id=claim_id)
    if db_claim is None:
        return ClaimResponse(status_code=404, success=False, message=f"Claim with id {claim_id} not found")

    return ClaimResponse(status_code=200, success=True, message="Claim successfully found", claim=db_claim)


def get_active_claim_by_claim_number(db_session: Session, claim_number: str) -> ClaimResponse:
    if claim_number is None:
        return ClaimResponse(status_code=400, success=False, message="Claim number cannot be null")
    db_claim_number = claim_repository.find_active_claim_by_claim_number(db_session=db_session, claim_number=claim_number)
    if db_claim_number is None:
        return ClaimResponse(status_code=404, success=False, message=f"Claim with number {claim_number} not found")

    return ClaimResponse(status_code=200, success=True, message="Claim successfully found", claim=db_claim_number)


def get_active_claim_by_policy_id(db_session: Session, policy_id: int) -> ClaimResponse:
    if policy_id is None:
        return ClaimResponse(status_code=400, success=False, message="Policy ID cannot be null")
    db_policy_id = claim_repository.find_active_claim_by_policy_id(db_session=db_session, policy_id=policy_id)
    if db_policy_id is None:
        return ClaimResponse(status_code=404, success=False, message=f"Claim for policy ID {policy_id} not found")

    return ClaimResponse(status_code=200, success=True, message="Claim successfully found", claim=db_policy_id)


def get_active_claim_by_user_id(db_session: Session, user_id: int) -> ClaimResponse:
    if user_id is None:
        return ClaimResponse(status_code=400, success=False, message="User ID cannot be null")
    db_user_id = claim_repository.find_active_claim_by_user_id(db_session=db_session, user_id=user_id)
    if db_user_id is None:
        return ClaimResponse(status_code=404, success=False, message=f"Claim for user ID {user_id} not found")

    return ClaimResponse(status_code=200, success=True, message="Claim successfully found", claim=db_user_id)


def get_all_active_claims(db_session: Session) -> ClaimResponse:
    db_claims = claim_repository.find_all_active_claims(db_session=db_session)
    if db_claims is None:
        return ClaimResponse(status_code=404, success=False, message="Claims not found")

    return ClaimResponse(status_code=200, success=True, message="Claims successfully found", claims=db_claims)


def create_claim(db_session: Session, create_request: ClaimCreate) -> ClaimResponse:
    existing_user = user_repository.find_active_user_by_id(db_session=db_session, user_id=create_request.user_id)

    if not existing_user:
        return ClaimResponse(status_code=404, success=False, message=f"User ID {create_request.user_id} not found")

    db_claim_response = get_active_claim_by_claim_number(db_session=db_session, claim_number=create_request.claim_number)

    if db_claim_response.success:
        return ClaimResponse(status_code=400, success=False, message="Claim number already exists")

    claim_entity: ClaimEntity = ClaimEntity(**create_request.dict())
    db_session.add(claim_entity)
    db_session.commit()
    db_session.refresh(claim_entity)

    return ClaimResponse(status_code=200, success=True, message="Claim created successfully", claim=claim_entity)


def update_claim(db_session: Session, claim_id:int, update_request: ClaimUpdate) -> ClaimResponse:
    existing_claim = claim_repository.find_active_claim_by_id(db_session=db_session, claim_id=claim_id)

    if not existing_claim:
        return ClaimResponse(status_code=404, success=False, message=f"Claim with ID {claim_id} not found")

    if update_request.claim_number != existing_claim.claim_number:
        claim_with_the_same_number = claim_repository.find_active_claim_by_claim_number(db_session=db_session, claim_number=update_request.claim_number)

        if claim_with_the_same_number:
            return ClaimResponse(status_code=400, success=False, message=f"Claim number '{update_request.claim_number}' already exists")

    update_dict = update_request.dict(exclude_unset=True)

    for key, value in update_dict.items():
        if value is not None and hasattr(existing_claim, key):
            setattr(existing_claim, key, value)

    db_session.commit()
    db_session.refresh(existing_claim)
    return ClaimResponse(status_code=200, success=True, message="Claim edited successfully", claim=existing_claim)


def delete_claim(db_session: Session, claim_id: int) -> ClaimResponse:
    existing_claim = claim_repository.find_active_claim_by_id(db_session=db_session, claim_id=claim_id)

    if existing_claim is None:
        return ClaimResponse(status_code=404, success=False, message=f"Claim with ID {claim_id} does not exist")

    existing_claim.entity_status = EntityStatus.DELETED
    db_session.delete(existing_claim)
    db_session.commit()

    return ClaimResponse(status_code=201, message="Claim successfully deleted", success=True, claim=existing_claim)