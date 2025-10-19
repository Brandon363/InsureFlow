# Document Storage

This directory contains all uploaded documents for the insurance application.

## Directory Structure


Documents/                
├── claim_documents/       # Claim-related documents (accident reports, damage photos, etc.)                                                  
└── supporting_documents/  # Personal documents (IDs, licenses, registration, etc.)


## Document Types

### Claim Documents (`CLAIM_DOCUMENT`)
Documents directly related to insurance claims:
- Accident reports
- Damage photos
- Police reports
- Medical reports
- Repair invoices
- Any other claim-specific documentation

### Supporting Documents (`SUPPORTING_DOCUMENT`)
Personal identification and supporting documents:
- National ID cards
- Driver's licenses
- Vehicle registration documents
- Proof of ownership
- Any other personal documentation

## File Storage

Files are automatically stored in the appropriate directory based on their `DocumentType`:
- `CLAIM_DOCUMENT` → `claim_documents/`
- `SUPPORTING_DOCUMENT` → `supporting_documents/`

Each file is given a unique filename (12-character UUID + original extension) to prevent conflicts while preserving the original filename in the database.

## API Usage

### Upload a Document

\`\`\`bash
curl -X POST "http://localhost:8000/document/upload-document" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/document.pdf" \
  -F "user_id=1" \
  -F "type=CLAIM_DOCUMENT" \
  -F "claim_id=123"
\`\`\`

### Get Documents by Claim

\`\`\`bash
curl -X GET "http://localhost:8000/document/get-active-documents-by-claim/123"
\`\`\`

### Get Documents by User

\`\`\`bash
curl -X GET "http://localhost:8000/document/get-active-documents-by-user/1"
\`\`\`

## Database Storage

Document metadata is stored in the `documents` table:
- `id`: Primary key
- `user_id`: User who uploaded the document
- `claim_id`: Associated claim (if applicable)
- `policy_id`: Associated policy (if applicable)
- `type`: Document type (CLAIM_DOCUMENT or SUPPORTING_DOCUMENT)
- `name`: Original filename
- `url`: Relative path to stored file
- `mime_type`: File MIME type
- `size`: File size in bytes
- `date_created`: Upload timestamp
- `date_updated`: Last update timestamp
- `entity_status`: ACTIVE, INACTIVE, or DELETED

## File Deletion

When a document is deleted via the API, both the physical file and database record are removed (soft delete for database, hard delete for file).
