from typing import Annotated
from fastapi import APIRouter
from fastapi.params import Depends
from requests import Session
from Config.database import get_db
from Model.UserModel import UserResponse, UserCreateRequest, UserUpdateRequest
from Service import UserService

router = APIRouter(
    prefix="/user"
)


db_dependency = Annotated[Session, Depends(get_db)]


@router.get('/get-active-user-by-id/{user_id}', response_model=None)
def get_active_user_by_id(user_id: int, db: db_dependency):
    return UserService.get_active_user_by_id(db_session=db, user_id=user_id)


@router.get('/get-active-user-by-id-number/{id_number}', response_model=None)
def get_active_user_by_id_number(id_number: str, db: db_dependency):
    return UserService.get_active_user_by_id_number(db_session=db, id_number=id_number)


@router.get('/get-all-active-users', response_model=None)
def get_all_active_users(db: db_dependency):
    return UserService.get_all_active_users(db_session=db)


@router.post('/create-user', response_model=None)
def create_user (create_request: UserCreateRequest, db: db_dependency):
    return UserService.create_user(db_session=db, create_request=create_request)


@router.put('update-user/{user_id}', response_model=None)
def update_user (update_request: UserUpdateRequest, user_id: int, db: db_dependency):
    return UserService.update_user(db_session=db, update_request=update_request)


@router.delete('delete-user/{user_id}', response_model=None)
def delete_user (user_id: int, db: db_dependency) -> UserResponse:
    return UserService.delete_user(db_session=db,user_id=user_id)