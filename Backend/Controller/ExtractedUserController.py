from typing import Annotated, List

from fastapi import APIRouter
from fastapi.params import Depends, Form, File
from requests import Session
from fastapi import UploadFile

from Config.database import get_db
from Model.ExtractedUserModel import ExtractedUserResponse, ExtractedUserCreateRequest, UserExtractRequest
from Service import ExtractedUserService

router = APIRouter(
    prefix="/extracted_user"
)


db_dependency = Annotated[Session, Depends(get_db)]


@router.get('/get-active-extracted-user-by-id/{extracted_user_id}', response_model=ExtractedUserResponse)
def get_active_user_by_id(extracted_user_id: int, db: db_dependency):
    return ExtractedUserService.get_active_extracted_user_by_id(db_session=db, extracted_user_id=extracted_user_id)

@router.get('/get-active-extracted-user-by-user-id/{user_id}', response_model=ExtractedUserResponse)
def get_active_user_by_id_number(user_id: int, db: db_dependency):
    return ExtractedUserService.get_active_extracted_user_by_user_id(db_session=db, user_id=user_id)


@router.get('/get-all-active-extracted-users', response_model=ExtractedUserResponse)
def get_all_active_users(db: db_dependency):
    return ExtractedUserService.get_all_active_extracted_users(db_session=db)


@router.post('/create-extracted-user', response_model=ExtractedUserResponse)
def create_user (create_request: ExtractedUserCreateRequest, db: db_dependency):
    return ExtractedUserService.create_extracted_user(db_session=db, create_request=create_request)


@router.delete('/delete-extracted-user/{user_id}', response_model=None)
def delete_user (user_id: int, db: db_dependency) -> ExtractedUserResponse:
    return ExtractedUserService.delete_extracted_user(db_session=db,user_id=user_id)


@router.post('/extract-user/{user_id}', response_model=ExtractedUserResponse)
async def extract_user(user_id: int, db: db_dependency,image_files: List[UploadFile] = File([])):
    image_file = image_files[0] if image_files else None
    return await ExtractedUserService.extract_user(db_session=db, image_file=image_file, user_id=user_id)

# @router.post('/extract-user', response_model=ExtractedUserResponse)
# async def extract_user(request: UserExtractRequest, db:db_dependency):
#     image_file = request.image_file
#     user_id = request.user_id
#     return await ExtractedUserService.extract_user(db_session=db, image_file=image_file, user_id=user_id)