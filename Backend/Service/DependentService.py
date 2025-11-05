from typing import List

from sqlalchemy.orm import Session
from Entity.DependentEntity import DependentEntity
from Model.DependentModel import DependentResponse, DependentCreateRequest, DependentUpdateRequest
from Repository import DependentRepository
from Utils.Enums import EntityStatus

def get_dependent_by_id(db_session: Session, dependent_id: int) -> DependentResponse:
    if dependent_id is None:
        return DependentResponse(status_code=400, success=False, message="Dependent ID cannot be null")

    db_dependent = DependentRepository.find_dependent_by_id(db_session=db_session, dependent_id=dependent_id)

    if db_dependent is None:
        return DependentResponse(status_code=404, success=False, message=f"Dependent with id {dependent_id} not found")

    return DependentResponse(status_code=200, success=True, message="Dependent successfully found", dependent=db_dependent)


def get_dependents_by_application_id(db_session: Session, application_id: int) -> DependentResponse:
    if application_id is None:
        return DependentResponse(status_code=400, success=False, message="Application ID cannot be null")

    db_dependents = DependentRepository.find_dependents_by_application_id(db_session=db_session, application_id=application_id)

    if db_dependents is None:
        return DependentResponse(status_code=404, success=False, message=f"Dependents for application {application_id} not found")

    return DependentResponse(status_code=200, success=True, message="Dependents successfully found", dependents=db_dependents)


def create_dependent(db_session: Session, create_request: DependentCreateRequest) -> DependentResponse:
    dependent_entity = DependentEntity()

    for key, value in create_request.dict().items():
        if hasattr(dependent_entity, key):
            setattr(dependent_entity, key, value)

    db_session.add(dependent_entity)
    db_session.commit()
    db_session.refresh(dependent_entity)

    return DependentResponse(status_code=201, success=True, message="Dependent created successfully", dependent=dependent_entity)


def create_multiple_dependents(db_session: Session, create_requests: List[DependentCreateRequest]) -> DependentResponse:
    # try:
    dependent_entities = []
    for create_request in create_requests:
        dependent_entity = DependentEntity(**create_request.dict())
        db_session.add(dependent_entity)
        dependent_entities.append(dependent_entity)

    db_session.commit()
    for dependent_entity in dependent_entities:
        db_session.refresh(dependent_entity)

    return DependentResponse(status_code=201, success=True, message="Dependents created successfully",
                             dependents=dependent_entities)



def update_dependent(db_session: Session, dependent_id: int, update_request: DependentUpdateRequest) -> DependentResponse:
    db_dependent = DependentRepository.find_dependent_by_id(db_session=db_session, dependent_id=dependent_id)

    if not db_dependent:
        return DependentResponse(status_code=404, success=False, message=f"Dependent with id {dependent_id} not found")

    update_dict = update_request.dict(exclude_unset=True)

    for key, value in update_dict.items():
        if value is not None and hasattr(db_dependent, key):
            setattr(db_dependent, key, value)

    db_session.commit()
    db_session.refresh(db_dependent)
    return DependentResponse(status_code=200, success=True, message="Dependent successfully updated", dependent=db_dependent)


def update_multiple_dependents(db_session: Session, update_requests: List[DependentUpdateRequest]) -> DependentResponse:
    dependent_entities = []
    for update_request in update_requests:
        dependent_entity = db_session.query(DependentEntity).get(update_request.id)
        if dependent_entity:
            update_dict = update_request.dict(exclude_unset=True)
            for key, value in update_dict.items():
                if key != "id" and hasattr(dependent_entity, key):
                    setattr(dependent_entity, key, value)
            dependent_entities.append(dependent_entity)
        else:
            #dependent was not found
            pass

    db_session.commit()
    for dependent_entity in dependent_entities:
        db_session.refresh(dependent_entity)

    return DependentResponse(status_code=200, success=True, message="Dependents updated successfully",
                             dependents=dependent_entities)


def delete_dependent(db_session: Session, dependent_id: int) -> DependentResponse:
    existing_dependent = DependentRepository.find_dependent_by_id(db_session=db_session, dependent_id=dependent_id)

    if existing_dependent is None:
        return DependentResponse(status_code=404, success=False, message="Dependent does not exist")

    existing_dependent.entity_status = EntityStatus.DELETED
    db_session.commit()

    return DependentResponse(status_code=201, success=True, message="Dependent successfully deleted", dependent=existing_dependent)