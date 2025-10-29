from typing import List

from sqlalchemy.orm import Session
from Entity.ExtractedDependentEntity import ExtractedDependentEntity
from Repository import ExtractedDependentRepository
from Model.ExtractedDependentModel import ExtractedDependentResponse, ExtractedDependentCreateRequest, \
    ExtractedDependentUpdateRequest
from Utils.Enums import EntityStatus


def get_active_extracted_dependent_by_id(db_session: Session,
                                         extracted_dependent_id: int) -> ExtractedDependentResponse:
    if extracted_dependent_id is None:
        return ExtractedDependentResponse(status_code=400, success=False,
                                          message="Extracted dependent ID cannot be null")

    db_extracted_dependent = ExtractedDependentRepository.find_active_extracted_dependent_by_id(db_session=db_session,
                                                                                                extracted_dependent_id=extracted_dependent_id)
    if db_extracted_dependent is None:
        return ExtractedDependentResponse(status_code=404, success=False,
                                          message=f"Extracted dependent with id {extracted_dependent_id} not found")

    return ExtractedDependentResponse(status_code=200, success=True, message="Extracted dependent successfully found",
                                      extracted_dependent=db_extracted_dependent)


def get_all_active_extracted_dependents(db_session: Session) -> ExtractedDependentResponse:
    db_extracted_dependents = ExtractedDependentRepository.find_all_active_extracted_dependents(db_session=db_session)

    if db_extracted_dependents is None:
        return ExtractedDependentResponse(status_code=404, success=False, message=f"Extracted dependents not found")

    return ExtractedDependentResponse(status_code=200, success=True, message="Extracted dependents successfully found",
                                      extracted_dependents=db_extracted_dependents)


def create_extracted_dependent(db_session: Session,
                               create_request: ExtractedDependentCreateRequest) -> ExtractedDependentResponse:
    extracted_dependent_entity = ExtractedDependentEntity(**create_request.dict())
    db_session.add(extracted_dependent_entity)
    db_session.commit()
    db_session.refresh(extracted_dependent_entity)

    return ExtractedDependentResponse(status_code=201, success=True, message="Extracted dependent created successfully",
                                      extracted_dependent=extracted_dependent_entity)


def create_multiple_extracted_dependents(db_session: Session, create_requests: List[
    ExtractedDependentCreateRequest]) -> ExtractedDependentResponse:
    extracted_dependent_entities = []
    for create_request in create_requests:
        extracted_dependent_entity = ExtractedDependentEntity(**create_request.dict())
        db_session.add(extracted_dependent_entity)
        extracted_dependent_entities.append(extracted_dependent_entity)

    db_session.commit()
    for extracted_dependent_entity in extracted_dependent_entities:
        db_session.refresh(extracted_dependent_entity)

    return ExtractedDependentResponse(
        status_code=201,
        success=True,
        message="Extracted dependents created successfully",
        extracted_dependents=extracted_dependent_entities
    )


def update_extracted_dependent(db_session: Session, extracted_dependent_id: int,
                               update_request: ExtractedDependentUpdateRequest) -> ExtractedDependentResponse:
    existing_extracted_dependent = ExtractedDependentRepository.find_active_extracted_dependent_by_id(
        db_session=db_session, extracted_dependent_id=extracted_dependent_id)

    if not existing_extracted_dependent:
        return ExtractedDependentResponse(status_code=404, success=False,
                                          message=f"Extracted dependent with id {extracted_dependent_id} not found")

    update_dict = update_request.dict(exclude_unset=True)

    for key, value in update_dict.items():
        if value is not None and hasattr(existing_extracted_dependent, key):
            setattr(existing_extracted_dependent, key, value)

    db_session.commit()
    db_session.refresh(existing_extracted_dependent)
    return ExtractedDependentResponse(status_code=200, success=True, message="Extracted dependent updated successfully",
                                      extracted_dependent=existing_extracted_dependent)


def delete_extracted_dependent(db_session: Session, extracted_dependent_id: int) -> ExtractedDependentResponse:
    existing_extracted_dependent = ExtractedDependentRepository.find_active_extracted_dependent_by_id(db_session,
                                                                                                      extracted_dependent_id)

    if existing_extracted_dependent is None:
        return ExtractedDependentResponse(status_code=404, message="Extracted dependent not found", success=False)

    existing_extracted_dependent.entity_status = EntityStatus.DELETED

    db_session.commit()
    db_session.refresh(existing_extracted_dependent)

    return ExtractedDependentResponse(status_code=201, message="Extracted dependent successfully deleted", success=True,
                                      extracted_dependent=existing_extracted_dependent)
