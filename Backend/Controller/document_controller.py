from fastapi import APIRouter
from fastapi.params import Depends
from requests import Session
from typing import Annotated

from Config.database import get_db
from Model.DocumentModel import DocumentResponse, DocumentCreate, DocumentUpdate
from Service import DocumentService

router = APIRouter(
    prefix="/document",
)


db_dependency = Annotated[Session, Depends(get_db)]


@router.get('/get-active-document-by-id{document_id}', response_model=None)
def get_active_document_by_id(document_id: int, db: db_dependency):
    return DocumentService.get_active_document_by_id(db_session=db, document_id=document_id)


@router.get('/get-active-document-by-user-id{user_id}', response_model=None)
def get_active_document_by_user_id(user_id: int, db: db_dependency):
    return DocumentService.get_active_document_by_user_id(db_session=db, user_id=user_id)


@router.get('/get-active-document-by-claim-id{claim_id}', response_model=None)
def get_active_document_by_claim_id(claim_id: int, db: db_dependency):
    return DocumentService.get_active_document_by_claim_id(db_session=db, claim_id=claim_id)


@router.get('/get-active-document-by-policy-id{policy_id}', response_model=None)
def get_active_document_by_policy_id(policy_id: int, db: db_dependency):
    return DocumentService.get_active_document_by_policy_id(db_session=db, policy_id=policy_id)


@router.get('/get-all-active-documents', response_model=None)
def get_all_active_documents(db: db_dependency):
    return DocumentService.get_all_active_documents(db_session=db)


@router.post('/create-document', response_model=None)
def create_document (create_request: DocumentCreate, db: db_dependency):
    return DocumentService.create_document(db_session=db, create_request=create_request)


@router.put('update-document/{document_id}', response_model=None)
def update_document (update_request: DocumentUpdate, document_id: int, db: db_dependency):
    return DocumentService.update_document(db_session=db, update_request=update_request)


@router.delete('delete-document/{document_id}', response_model=None)
def delete_document (document_id: int, db: db_dependency) -> DocumentResponse:
    return DocumentService.delete_document(db_session=db,document_id=document_id)

