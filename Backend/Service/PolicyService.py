from sqlalchemy.orm import Session
from Entity import PolicyEntity
from Model.PolicyModel import PolicyResponse, PolicyCreateRequest, PolicyUpdateRequest
from Repository import policy_repository
from Utils.Enums import EntityStatus


def get_active_policy_by_id(db_session: Session, policy_id: int) -> PolicyResponse:
    if policy_id is None:
        return PolicyResponse(status_code=400, success=False, message="Policy ID cannot be null")

    db_policy = policy_repository.find_active_policy_by_id(db_session=db_session, policy_id=policy_id)
    if db_policy is None:
        return PolicyResponse(status_code=404, success=False, message=f"Policy with id {policy_id} not found")

    return PolicyResponse(status_code=200, success=True, message="Policy successfully found", policy=db_policy)


def get_active_policy_by_policy_number(db_session, policy_number: str) -> PolicyResponse:
    if policy_number is None:
        return PolicyResponse(status_code=400, success=False, message="Policy number cannot be null")

    db_policy = policy_repository.find_active_policy_by_policy_number(db_session=db_session, policy_number=policy_number)
    if db_policy is None:
        return PolicyResponse(status_code=404, success=False, message=f"Policy with id {policy_number} not found")

    return PolicyResponse(status_code=200,success=True, message="Policy successfully found", policy=db_policy)


def get_active_policy_by_user_id(db_session: Session, user_id: int) -> PolicyResponse:
    if user_id is None:
        return PolicyResponse(status_code=400, success=False, message="User ID cannot be null")

    db_policy = policy_repository.find_active_policy_by_user_id(db_session=db_session, user_id=user_id)
    if db_policy is None:
        return PolicyResponse(status_code=404, success=False, message=f"Policy for user with user id {user_id} not found")

    return PolicyResponse(status_code=200,success=True, message="Policy successfully found", policy=db_policy)


def get_all_active_policies(db_session: Session) -> PolicyResponse:
    db_policies = policy_repository.find_all_active_policies(db_session=db_session)

    if db_policies is None:
        return PolicyResponse(status_code=404, success=False, message=f"Policies not found")

    return PolicyResponse(status_code=200, success=True, message="Policies successfully found", policies=db_policies)


def create_policy(db_session: Session, create_request: PolicyCreateRequest) -> PolicyResponse:
    db_policy_response = get_active_policy_by_id(db_session=db_session, policy_id=create_request.policy_number)

    if db_policy_response.success:
        return PolicyResponse(status_code=400, success=False, message="Policy number already exists")

    policy_entity: PolicyEntity = PolicyEntity(**create_request.dict())
    db_session.add(policy_entity)
    db_session.commit()
    db_session.refresh(policy_entity)

    return PolicyResponse(status_code=201, success=True, message="Policy created successfully", policy=policy_entity)


def update_policy(db_session: Session, update_request: PolicyUpdateRequest) -> PolicyResponse:
    db_policy = policy_repository.find_active_policy_by_policy_number(db_session=db_session, policy_number=update_request.policy_number)

    if db_policy and db_policy.id != update_request.id:
        return PolicyResponse(status_code=400, success=False, message="Policy number already exists")

    update_dict = update_request.dict(exclude_unset=True)

    for key, value in update_dict.items():
        if value is not None:
            setattr(db_policy, key, value)

    db_session.commit()
    db_session.refresh(db_policy)
    return PolicyResponse(status_code=200, success=True, message="Policy successfully updated", policy =db_policy)


def delete_policy(db_session: Session, policy_id: int) -> PolicyResponse:
    existing_policy = policy_repository.find_active_policy_by_id(db_session=db_session, policy_id=policy_id)

    if existing_policy is None:
        return PolicyResponse(status_code=404, success=False, message="Policy does not exist")

    existing_policy.entity_status = EntityStatus.DELETED
    db_session.delete(existing_policy)
    db_session.commit()

    return PolicyResponse(status_code=201, success=True, message="Policy successfully deleted", policy =existing_policy)