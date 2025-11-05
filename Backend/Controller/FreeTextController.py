from typing import Annotated, List

from fastapi import APIRouter
from fastapi.params import Depends, Form, File
from requests import Session
from fastapi import UploadFile

from Config.database import get_db
from Model.ExtractedUserModel import ExtractedUserResponse, ExtractedUserCreateRequest, UserExtractRequest
from Service import FreeTextService
from Service.FreeTextService import ExtractedTextResponse

router = APIRouter(
    prefix="/free_text"
)


db_dependency = Annotated[Session, Depends(get_db)]

@router.post('/free-text', response_model=ExtractedTextResponse)
async def extract_user(db: db_dependency,image_files: List[UploadFile] = File([])):
    image_file = image_files[0] if image_files else None
    return await FreeTextService.analyze_read(db_session=db, image_file=image_file)
