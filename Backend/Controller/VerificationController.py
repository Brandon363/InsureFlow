from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from Config.database import get_db
from Model.VerificationModel import VerificationResponse
from Service import VerificationService

router = APIRouter(
    prefix="/verification"
)

db_dependency = Annotated[Session, Depends(get_db)]


@router.get('/get-all-active-verified-users', response_model=VerificationResponse)
def get_all_active_verified_users(id_number: str, first_name: str = None, last_name: str = None,
    email: str = None, phone_number: str = None, db: db_dependency = None):
    return VerificationService.get_all_active_verified_users(db_session=db, id_number=id_number,
        first_name=first_name, last_name=last_name, email=email, phone_number=phone_number)
