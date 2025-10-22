from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from Config.database import get_db
from Model.DocumentModel import DocumentResponse, DocumentCreate, DocumentUpdate
from Service import DocumentService
from Utils.Enums import DocumentType

router = APIRouter(
    prefix="/document"
)

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document_by_id(document_id: int, db: db_dependency):
    return DocumentService.get_active_document_by_id(db_session=db, document_id=document_id)


@router.get("/claim/{claim_id}", response_model=DocumentResponse)
def get_documents_by_claim_id(claim_id: int, db: db_dependency):
    return DocumentService.get_active_documents_by_claim_id(db_session=db, claim_id=claim_id)


@router.get("/user/{user_id}", response_model=DocumentResponse)
def get_documents_by_user_id(user_id: int, db: db_dependency):
    return DocumentService.get_active_documents_by_user_id(db_session=db, user_id=user_id)


@router.get("/policy/{policy_id}", response_model=DocumentResponse)
def get_documents_by_policy_id(policy_id: int, db: db_dependency):
    return DocumentService.get_active_documents_by_policy_id(db_session=db, policy_id=policy_id)


@router.get("/get-all-documents", response_model=DocumentResponse)
def get_all_documents(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: db_dependency = None):
    return DocumentService.get_all_active_documents(db_session=db)


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...), user_id: int = Form(...),
                          document_type: DocumentType = Form(...), claim_id: int = Form(None),
                          policy_id: int = Form(None), db: Session = Depends(get_db)):
    # Upload a document file with metadata
    return await DocumentService.upload_document(db_session=db, file=file,
                                                 user_id=user_id, document_type=document_type, claim_id=claim_id,
                                                 policy_id=policy_id)


@router.post("/create-document", response_model=DocumentResponse)
def create_document(create_request: DocumentCreate, db: db_dependency):
    return DocumentService.create_document(db_session=db, create_request=create_request)


@router.put("/{document_id}", response_model=DocumentResponse)
def update_document(
        document_id: int,
        update_request: DocumentUpdate,
        db: db_dependency
):
    return DocumentService.update_document(
        db_session=db,
        document_id=document_id,
        update_request=update_request
    )


@router.get("/get-document-file-by-id/{document_id}")
def get_document_file_by_id(document_id: int, db: db_dependency):
    return DocumentService.get_document_file_by_id(db, document_id)


@router.get("/get-id-document-file-by-id/{user_id}")
def get_id_document_file_by_user_id(user_id: int, db: db_dependency):
    return DocumentService.get_id_document_file_by_user_id(db_session=db, user_id=user_id)


@router.delete("/{document_id}", response_model=DocumentResponse)
def delete_document(document_id: int, db: db_dependency):
    return DocumentService.delete_document(db_session=db, document_id=document_id)
