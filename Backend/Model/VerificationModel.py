from pydantic import BaseModel
from typing import List, Optional
from Utils.Enums import VerificationStatus


class VerifiedUserDTO(BaseModel):
    id: int
    id_number: str
    first_name: str
    last_name: str
    other_names: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    verification_status: VerificationStatus


class VerificationResponse(BaseModel):
    status_code: int
    success: bool
    message: str
    query_id_number: Optional[str] = None
    total_matches: Optional[int] = 0
    has_exact_match: Optional[bool] = False
    matches: Optional[List[VerifiedUserDTO]] = []
