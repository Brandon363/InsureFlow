from typing import Annotated
from fastapi import APIRouter
from fastapi.params import Depends
from requests import Session
from Config.database import get_db
from Model.UserModel import UserResponse, UserCreateRequest, UserUpdateRequest, UserLoginRequest, UserPasswordUpdate
from Service import UserService

router = APIRouter(
    prefix="/user"
)


db_dependency = Annotated[Session, Depends(get_db)]


@router.get('/get-active-user-by-id/{user_id}', response_model=UserResponse)
def get_active_user_by_id(user_id: int, db: db_dependency):
    return UserService.get_active_user_by_id(db_session=db, user_id=user_id)

@router.get('/is-user-logged-in/{user_id}', response_model=UserResponse)
def is_user_logged_in(user_id: int, db: db_dependency):
    return UserService.is_user_logged_in(db_session=db, user_id=user_id)


@router.get('/get-active-user-by-id-number/{id_number}', response_model=UserResponse)
def get_active_user_by_id_number(id_number: str, db: db_dependency):
    return UserService.get_active_user_by_id_number(db_session=db, id_number=id_number)


@router.get('/get-active-user-by-email/{email}', response_model=UserResponse)
def get_active_user_by_email(email: str, db: db_dependency):
    return UserService.get_active_user_by_email(db_session=db, email=email)


@router.get('/get-all-active-users', response_model=UserResponse)
def get_all_active_users(db: db_dependency):
    return UserService.get_all_active_users(db_session=db)


@router.post('/create-user', response_model=UserResponse)
def create_user (create_request: UserCreateRequest, db: db_dependency):
    return UserService.create_user(db_session=db, create_request=create_request)


@router.post('/login', response_model=UserResponse)
def login_user(login_request: UserLoginRequest, db: db_dependency):
    return UserService.login_user(db_session=db, login_request=login_request)


@router.post('/logout/{user_id}', response_model=UserResponse)
def logout_user(user_id: int, db: db_dependency):
    return UserService.logout_user(db_session=db, user_id=user_id)


@router.put('/update-user/{user_id}', response_model=UserResponse)
def update_user (user_id: int, update_request: UserUpdateRequest, db: db_dependency):
    return UserService.update_user(db_session=db, user_id=user_id, update_request=update_request)


@router.put('/update-password/{user_id}', response_model=UserResponse)
def update_password(user_id: int, password_update: UserPasswordUpdate, db: db_dependency):
    return UserService.update_user_password(db_session=db, user_id=user_id, password_update=password_update)


@router.delete('/delete-user/{user_id}', response_model=None)
def delete_user (user_id: int, db: db_dependency) -> UserResponse:
    return UserService.delete_user(db_session=db,user_id=user_id)