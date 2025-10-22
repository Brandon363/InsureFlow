from pathlib import Path

import aiofiles
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
from fastapi.responses import StreamingResponse

from Entity import UserEntity, ClaimEntity, PolicyEntity
from Model.DocumentModel import DocumentCreate, DocumentUpdate, DocumentResponse
from Entity.DocumentEntity import DocumentEntity
from Repository import document_repository
from Utils.Enums import EntityStatus, DocumentType
from Utils.FileStorage import save_uploaded_file, delete_file
from datetime import datetime


def _validate_user_exists(db_session: Session, user_id: int):
    # Validate that the user exists
    user = db_session.query(UserEntity).filter(
        UserEntity.id == user_id, UserEntity.entity_status == EntityStatus.ACTIVE).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")


def _validate_claim_exists(db_session: Session, claim_id: int):
    # Validate that the claim exists if provided
    if claim_id is not None:
        claim = db_session.query(ClaimEntity).filter(
            ClaimEntity.id == claim_id, ClaimEntity.entity_status == EntityStatus.ACTIVE).first()
        if not claim:
            raise HTTPException(status_code=404, detail=f"Claim with ID {claim_id} not found")


def _validate_policy_exists(db_session: Session, policy_id: int):
    # Validate that the policy exists if provided
    if policy_id is not None:
        policy = db_session.query(PolicyEntity).filter(
            PolicyEntity.id == policy_id, PolicyEntity.entity_status == EntityStatus.ACTIVE).first()
        if not policy:
            raise HTTPException(status_code=404, detail=f"Policy with ID {policy_id} not found")


def _validate_document_exists(document, document_id: int):
    # Helper to validate document existence
    if not document:
        raise HTTPException(status_code=404, detail=f"Document with ID {document_id} not found")


def _validate_id_not_null(entity_id: int, entity_name: str):
    # Helper to validate ID is not null
    if entity_id is None:
        raise HTTPException(status_code=400, detail=f"{entity_name} ID cannot be null")


async def upload_document(db_session: Session, file: UploadFile, user_id: int,
                          document_type: DocumentType, claim_id: int = None, policy_id: int = None) -> DocumentResponse:
    # Upload a document file and save metadata to database

    # Save file to storage
    file_path, original_filename, file_size = await save_uploaded_file(file, document_type)

    # Create document entity
    new_document = DocumentEntity(
        user_id=user_id, claim_id=claim_id,
        policy_id=policy_id, type=document_type, name=original_filename, url=file_path,
        mime_type=file.content_type or "application/octet-stream",
        size=file_size, entity_status=EntityStatus.ACTIVE
    )

    db_session.add(new_document)
    db_session.commit()
    db_session.refresh(new_document)

    return DocumentResponse(status_code=201, success=True, message="Document uploaded successfully",
                            document=new_document)


def get_active_document_by_id(db_session: Session, document_id: int) -> DocumentResponse:
    _validate_id_not_null(document_id, "Document")

    document = document_repository.find_active_document_by_id(db_session, document_id)
    _validate_document_exists(document, document_id)

    return DocumentResponse(status_code=200, success=True, message="Document retrieved successfully", document=document)


def get_all_active_documents(db_session: Session) -> DocumentResponse:
    documents = document_repository.find_all_active_documents(db_session)

    return DocumentResponse(status_code=200, success=True, message="Documents retrieved successfully",
                            documents=documents or [])


def get_active_documents_by_claim_id(db_session: Session, claim_id: int) -> DocumentResponse:
    _validate_id_not_null(claim_id, "Claim")

    documents = document_repository.find_active_documents_by_claim_id(db_session, claim_id)

    return DocumentResponse(status_code=200, success=True, message="Documents retrieved successfully",
                            documents=documents or [])


def get_active_documents_by_user_id(db_session: Session, user_id: int) -> DocumentResponse:
    _validate_id_not_null(user_id, "User")

    documents = document_repository.find_active_documents_by_user_id(db_session, user_id)

    return DocumentResponse(status_code=200, success=True, message="Documents retrieved successfully",
                            documents=documents or [])


def get_active_documents_by_policy_id(db_session: Session, policy_id: int) -> DocumentResponse:
    _validate_id_not_null(policy_id, "Policy")

    documents = document_repository.find_active_documents_by_policy_id(db_session, policy_id)

    return DocumentResponse(status_code=200, success=True, message="Documents retrieved successfully",
                            documents=documents or [])


def create_document(db_session: Session, create_request: DocumentCreate) -> DocumentResponse:
    _validate_user_exists(db_session, create_request.user_id)
    _validate_claim_exists(db_session, create_request.claim_id)
    _validate_policy_exists(db_session, create_request.policy_id)

    new_document = DocumentEntity(user_id=create_request.user_id, claim_id=create_request.claim_id,
                                  policy_id=create_request.policy_id, type=create_request.type,
                                  name=create_request.name,
                                  url=create_request.url, mime_type=create_request.mime_type, size=create_request.size,
                                  entity_status=EntityStatus.ACTIVE)

    db_session.add(new_document)
    db_session.commit()
    db_session.refresh(new_document)

    return DocumentResponse(status_code=201, success=True, message="Document created successfully",
                            document=new_document)


def update_document(db_session: Session, document_id: int, update_request: DocumentUpdate) -> DocumentResponse:
    _validate_id_not_null(document_id, "Document")

    document = document_repository.find_active_document_by_id(db_session, document_id)
    _validate_document_exists(document, document_id)

    update_dict = update_request.dict(exclude_unset=True)

    for key, value in update_dict.items():
        if value is not None and hasattr(document, key):
            setattr(document, key, value)

    document.date_updated = datetime.utcnow()
    db_session.commit()
    db_session.refresh(document)

    return DocumentResponse(status_code=200, success=True, message="Document updated successfully", document=document)


def delete_document(db_session: Session, document_id: int) -> DocumentResponse:
    _validate_id_not_null(document_id, "Document")

    document = document_repository.find_active_document_by_id(db_session, document_id)
    _validate_document_exists(document, document_id)

    # Delete physical file
    delete_file(document.url)

    # Soft delete in database
    document.entity_status = EntityStatus.DELETED
    document.date_updated = datetime.utcnow()
    db_session.commit()

    return DocumentResponse(status_code=200, success=True, message="Document deleted successfully", document=document)


def get_document_file_by_id(db_session: Session, document_id: int):
    """Endpoint to stream a document file"""
    document = document_repository.find_active_document_by_id(db_session, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # file_path = Path(document.url)
    file_path = Path("backend") / document.url
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    # Security check - prevent directory traversal
    if not file_path.is_file() or not file_path.resolve().is_relative_to(Path("backend/Documents").resolve()):
        raise HTTPException(status_code=403, detail="Access denied")

    async def file_sender():
        async with aiofiles.open(file_path, 'rb') as f:
            while True:
                chunk = await f.read(65536)  # 64KB chunks
                if not chunk:
                    break
                yield chunk

    return StreamingResponse(
        file_sender(),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"inline; filename={document.name}",
            "Content-Length": str(file_path.stat().st_size)
        }
    )


def get_id_document_file_by_user_id(db_session: Session, user_id: int):
    """Endpoint to stream a document file"""
    document = document_repository.find_active_id_document_by_user_id(db_session, user_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    # print("document found", document)

    # file_path = Path(document.url)
    file_path = Path("backend") / document.url
    # print(file_path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    # Security check - prevent directory traversal
    if not file_path.is_file() or not file_path.resolve().is_relative_to(Path("backend/Documents").resolve()):
        raise HTTPException(status_code=403, detail="Access denied")

    async def file_sender():
        async with aiofiles.open(file_path, 'rb') as f:
            while True:
                chunk = await f.read(65536)  # 64KB chunks
                if not chunk:
                    break
                yield chunk

    return StreamingResponse(
        file_sender(),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"inline; filename={document.name}",
            "Content-Length": str(file_path.stat().st_size)
        }
    )