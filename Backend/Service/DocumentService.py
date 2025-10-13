from sqlalchemy.orm import Session
from Model.DocumentModel import DocumentCreate, DocumentUpdate, DocumentResponse
from Entity.DocumentEntity import DocumentEntity
from Repository import document_repository
from Utils.Enums import EntityStatus


def get_active_document_by_id(db_session: Session, document_id: int) -> DocumentResponse:
    if document_id is None:
        return DocumentResponse(status_code=400, success=False, message="Document ID cannot be null")
    db_document = document_repository.find_active_document_by_id(db_session=db_session, document_id=document_id)
    if db_document is None:
        return DocumentResponse(status_code=404, success=False, message=f"Document with id {document_id} not found")

    return DocumentResponse(status_code=200, success=True, message="Document successfully found", document=db_document)


def get_active_document_by_user_id(db_session: Session, user_id: int) -> DocumentResponse:
    if user_id is None:
        return DocumentResponse(status_code=400, success=False, message="User ID cannot be null")
    db_user_id = document_repository.find_active_document_by_user_id(db_session=db_session, user_id=user_id)
    if db_user_id is None:
        return DocumentResponse(status_code=404, success=False, message=f"Document for user ID {user_id} not found")

    return DocumentResponse(status_code=200, success=True, message="Document retrieved successfully", document=db_user_id)


def get_active_document_by_claim_id(db_session: Session, claim_id: int) -> DocumentResponse:
    if claim_id is None:
        return DocumentResponse(status_code=400, success=False, message="Claim ID cannot be null")
    db_claim = document_repository.find_active_claim_by_id(db_session=db_session, claim_id=claim_id)
    if db_claim is None:
        return DocumentResponse(status_code=404, success=False, message=f"Claim with id {claim_id} not found")

    return DocumentResponse(status_code=200, success=True, message="Claim successfully", claim=db_claim)


def get_active_document_by_policy_id(db_session: Session, policy_id: int) -> DocumentResponse:
    if policy_id is None:
        return DocumentResponse(status_code=400, success=False, message="Policy ID cannot be null")
    db_policy_id = document_repository.find_active_document_by_policy_id(db_session=db_session, policy_id=policy_id)
    if db_policy_id is None:
        return DocumentResponse(status_code=404, success=False, message=f"Document for policy ID {policy_id} not found")

    return DocumentResponse(status_code=200, success=True, message="Document successfully found", document=db_policy_id)


def get_all_active_documents(db_session: Session) -> DocumentResponse:
    db_documents = document_repository.find_all_active_documents(db_session=db_session)
    if db_documents is None:
        return DocumentResponse(status_code=404, success=False, message="Documents not found")

    return DocumentResponse(status_code=200, success=True, message="Documents successfully found", documents=db_documents)


def create_document(db_session: Session, create_request: DocumentCreate) -> DocumentResponse:
    db_document_response = get_active_document_by_id(db_session=db_session,
                                                         document_id=create_request.document_number)

    if db_document_response.success:
        return DocumentResponse(status_code=400, success=False, message="Document ID already exists")

    document_entity: DocumentEntity = DocumentEntity(**create_request.dict())
    db_session.add(document_entity)
    db_session.commit()
    db_session.refresh(document_entity)

    return DocumentResponse(status_code=201, success=True, message="Document created successfully", document=document_entity)


def update_document(db_session: Session, update_request: DocumentUpdate) -> DocumentResponse:
    db_document = document_repository.find_active_document_by_id(db_session=db_session,
                                                                  document_id=update_request.document_number)

    if db_document and db_document.id != update_request.id:
        return DocumentResponse(status_code=400, success=False, message="Document ID already exists")

    update_dict = update_request.dict(exclude_unset=True)
    for key, value in update_dict.items():
        if value is not None:
            setattr(db_document, key, value)

    db_session.commit()
    db_session.refresh(db_document)
    return DocumentResponse(status_code=201, success=True, message="Document edited successfully", document=db_document)


def delete_document(db_session: Session, document_id: int) -> DocumentResponse:
    existing_document = document_repository.find_active_document_by_id(db_session, document_id)

    if existing_document is None:
        return DocumentResponse(status_code=404, message=f"Document ID {document_id} not found", success=False)

    existing_document.entity_status = EntityStatus.DELETED

    db_session.commit()
    db_session.refresh(existing_document)
    return DocumentResponse(status_code=201, message="Document successfully deleted", success=True, document=existing_document)