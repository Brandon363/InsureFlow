from sqlalchemy.orm import Session
from Entity.UserEntity import UserEntity
from Model.UserModel import UserResponse, UserCreateRequest, UserUpdateRequest
from Repository import user_repository
from Utils.Enums import EntityStatus


def get_active_user_by_id(db_session: Session, user_id: int) -> UserResponse:
    if user_id is None:
        return UserResponse(status_code=400, success=False, message="User ID cannot be null")
    db_user = user_repository.find_active_user_by_id(db_session=db_session, user_id=user_id)
    if db_user is None:
        return UserResponse(status_code=404, success=False, message=f"User with id {user_id} not found")

    return UserResponse(status_code=200, success=True, message="User successfully found", user=db_user)


def get_active_user_by_id_number(db_session: Session, id_number: str) -> UserResponse:
    if id_number is None:
        return UserResponse(status_code=400, success=False, message="ID number cannot be null")

    db_user = user_repository.find_active_user_by_id_number(db_session=db_session, id_number=id_number)
    if db_user is None:
        return UserResponse(status_code=404, success=False, message=f"ID {id_number} not found")

    return UserResponse(status_code=200, success=True, message="User successfully found", user=db_user)


def get_all_active_users(db_session: Session) -> UserResponse:
    db_users = user_repository.find_all_active_users(db_session=db_session)

    if db_users is None:
        return UserResponse(status_code=404, success=False, message=f"Users not found")

    return UserResponse(status_code=200, success=True, message="Users successfully found", users=db_users)


def create_user(db_session: Session, create_request: UserCreateRequest) -> UserResponse:
    db_user_response = get_active_user_by_id_number(db_session=db_session, id_number=create_request.id_number)

    if db_user_response.success:
        return UserResponse(status_code=400, success=False, message="User id already exists")

    user_entity = UserEntity(**create_request.dict())
    # user_entity.is_logged_in = False
    db_session.add(user_entity)
    db_session.commit()
    db_session.refresh(user_entity)

    return UserResponse(status_code=201, success=True, message="User created successfully", user=user_entity)


def update_user(db_session: Session, update_request: UserUpdateRequest) -> UserResponse:
    db_user = user_repository.find_active_user_by_id(db_session=db_session, user_id=update_request.user_id)

    if db_user and db_user.id != update_request.id:
        return UserResponse(status_code=400, success=False, message="User id already exists")

    update_dict = update_request.dict(exclude_unset=True)

    for key, value in update_dict.items():
        if value is not None:
            setattr(db_user, key, value)

    db_session.commit()
    db_session.refresh(db_user)
    return UserResponse(status_code=200, success=True, message="User successfully updated", user=db_user)

def delete_user(db_session: Session, user_id: int) -> UserResponse:
    existing_user = user_repository.find_active_user_by_id(db_session=db_session, user_id=user_id)

    if existing_user is None:
        return UserResponse(status_code=404, success=False, message="User does not exist")

    existing_user.entity_status = EntityStatus.DELETED
    db_session.delete(existing_user)
    db_session.commit()

    return UserResponse(status_code=201, success=True, message="User successfully deleted", user=existing_user)