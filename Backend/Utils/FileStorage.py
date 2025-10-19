import uuid
from pathlib import Path
from typing import Tuple
from fastapi import UploadFile
from Utils.Enums import DocumentType

# Base directory for all documents
BASE_DOCUMENTS_DIR = Path("backend/Documents")
CLAIM_DOCUMENTS_DIR = BASE_DOCUMENTS_DIR / "claim_documents"
SUPPORTING_DOCUMENTS_DIR = BASE_DOCUMENTS_DIR / "supporting_documents"


def ensure_directories_exist():
    # Create document directories if they don't exist
    CLAIM_DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
    SUPPORTING_DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)


def get_storage_directory(document_type: DocumentType) -> Path:
    # Get the appropriate storage directory based on document type
    if document_type == DocumentType.CLAIM_DOCUMENT:
        return CLAIM_DOCUMENTS_DIR
    else:  # SUPPORTING_DOCUMENT
        return SUPPORTING_DOCUMENTS_DIR


def generate_unique_filename(original_filename: str) -> str:
    # Generate a unique filename while preserving the extension
    file_extension = Path(original_filename).suffix
    unique_id = uuid.uuid4().hex[:12]
    return f"{unique_id}{file_extension}"


async def save_uploaded_file(file: UploadFile, document_type: DocumentType) -> Tuple[str, str, int]:
    # Save an uploaded file to the appropriate directory

    ensure_directories_exist()

    # Generate unique filename
    unique_filename = generate_unique_filename(file.filename)

    # Get storage directory
    storage_dir = get_storage_directory(document_type)

    # Full file path
    file_path = storage_dir / unique_filename

    # Read and save file
    contents = await file.read()
    file_size = len(contents)

    with open(file_path, "wb") as f:
        f.write(contents)

    # Return relative path from backend root
    relative_path = str(file_path.relative_to(Path("backend")))

    return relative_path, file.filename, file_size


def delete_file(file_path: str) -> bool:
    # Delete a file from storage
    full_path = Path("backend") / file_path
    if full_path.exists():
        full_path.unlink()
        return True
    return False