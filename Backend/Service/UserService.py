from datetime import datetime

from sqlalchemy.orm import Session
from Entity.UserEntity import UserEntity
from Model.UserModel import UserResponse, UserCreateRequest, UserUpdateRequest, UserLoginRequest, UserPasswordUpdate
from Repository import user_repository
from Utils.Enums import EntityStatus, VerificationStatus


def get_active_user_by_id(db_session: Session, user_id: int) -> UserResponse:
    if user_id is None:
        return UserResponse(status_code=400, success=False, message="User ID cannot be null")
    db_user = user_repository.find_active_user_by_id(db_session=db_session, user_id=user_id)
    # print(db_user.extracted_users)
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


def get_active_user_by_email(db_session: Session, email: str) -> UserResponse:
    if email is None:
        return UserResponse(status_code=400, success=False, message="Email cannot be null")

    db_user = user_repository.find_active_user_by_email(db_session=db_session, email=email)
    if db_user is None:
        return UserResponse(status_code=404, success=False, message=f"User with email {email} not found")

    return UserResponse(status_code=200, success=True, message="User successfully found", user=db_user)


def get_all_active_users(db_session: Session) -> UserResponse:
    db_users = user_repository.find_all_active_users(db_session=db_session)

    if db_users is None:
        return UserResponse(status_code=404, success=False, message=f"Users not found")

    return UserResponse(status_code=200, success=True, message="Users successfully found", users=db_users)


def create_user(db_session: Session, create_request: UserCreateRequest) -> UserResponse:
    # Check if ID number already exists
    existing_user_by_id = user_repository.find_active_user_by_id_number(
        db_session=db_session, id_number=create_request.id_number.strip().replace(" ", "").upper())

    if existing_user_by_id:
        return UserResponse(status_code=400, success=False, message="ID number already exists")

    # Check if email already exists
    existing_user_by_email = user_repository.find_active_user_by_email(db_session=db_session, email=create_request.email)

    if existing_user_by_email:
        return UserResponse(status_code=400, success=False, message="Email already exists")

    # Create user entity
    user_entity = UserEntity()

    # Set basic attributes
    for key, value in create_request.dict().items():
        if key != 'password' and hasattr(user_entity, key):
            setattr(user_entity, key, value)

    # Hash and set password
    user_entity.set_password(create_request.password)

    db_session.add(user_entity)
    db_session.commit()
    db_session.refresh(user_entity)

    return UserResponse(status_code=201, success=True, message="User created successfully", user=user_entity)


def login_user(db_session: Session, login_request: UserLoginRequest) -> UserResponse:
    # Find user by email
    db_user = user_repository.find_active_user_by_email(db_session=db_session, email=login_request.email)

    if not db_user:
        return UserResponse(status_code=401, success=False, message="Invalid email or password")

    # Handle case where user has no password (shouldn't happen but safe check)
    if not db_user.check_password(login_request.password):
        return UserResponse(status_code=401, success=False, message="Account setup incomplete. Please contact administrator.")

    # Verify password
    if not db_user.check_password(login_request.password):
        return UserResponse(status_code=401, success=False, message="Invalid email or password")

    # Update login status
    db_user.is_logged_in = True
    db_user.date_last_logged_in = datetime.utcnow()
    db_session.commit()
    db_session.refresh(db_user)

    return UserResponse(status_code=200, success=True, message="Login successful", user=db_user)


def logout_user(db_session: Session, user_id: int) -> UserResponse:
    db_user = user_repository.find_active_user_by_id(db_session=db_session, user_id=user_id)

    if not db_user:
        return UserResponse(status_code=404, success=False, message="User not found")

    # Update logout status
    db_user.is_logged_in = False
    db_session.commit()
    db_session.refresh(db_user)

    return UserResponse(status_code=200, success=True, message="Logout successful", user=db_user)


def verify_user(db_session: Session, user_id: int) -> UserResponse:
    db_user: UserEntity | None = user_repository.find_active_user_by_id(db_session=db_session, user_id=user_id)

    if not db_user:
        return UserResponse(status_code=404, success=False, message="User not found")

    # Update verification status
    db_user.verification_status = VerificationStatus.VERIFIED
    db_session.commit()
    db_session.refresh(db_user)

    return UserResponse(status_code=200, success=True, message="User successful verified", user=db_user)


def make_user_verification_status_pending(db_session: Session, user_id: int) -> UserResponse:
    db_user: UserEntity | None = user_repository.find_active_user_by_id(db_session=db_session, user_id=user_id)

    if not db_user:
        return UserResponse(status_code=404, success=False, message="User not found")

    # Update verification status
    db_user.verification_status = VerificationStatus.PENDING
    db_session.commit()
    db_session.refresh(db_user)

    return UserResponse(status_code=200, success=True, message="User verification status successfully updated", user=db_user)


def update_user_password(db_session: Session, user_id: int, password_update: UserPasswordUpdate) -> UserResponse:
    db_user = user_repository.find_active_user_by_id(db_session=db_session, user_id=user_id)

    if not db_user:
        return UserResponse(status_code=404, success=False, message="User not found")

    # Verify old password
    if not db_user.check_password(password_update.old_password):
        return UserResponse(status_code=401, success=False, message="Invalid password")

    # Set new password
    db_user.set_password(password_update.new_password)
    db_session.commit()

    return UserResponse(status_code=200, success=True, message="Password updated successfully", user=db_user)


def update_user(db_session: Session, user_id:int, update_request: UserUpdateRequest) -> UserResponse:
    db_user = user_repository.find_active_user_by_id(db_session=db_session, user_id=user_id)

    if not db_user:
        return UserResponse(status_code=404, success=False, message=f"User with id {user_id} not found")

    # Check if ID number is being changed and conflicts with another user
    if update_request.id_number and update_request.id_number != db_user.id_number:
        user_with_same_id =user_repository.find_active_user_by_id_number(db_session=db_session, id_number=update_request.id_number)

        if user_with_same_id:
            return UserResponse(status_code=400, success=False, message=f"ID number '{update_request.id_number}' already exists")

    # Check if email is being changed and conflicts with another user
    if update_request.email and update_request.email != db_user.email:
        user_with_same_email = user_repository.find_active_user_by_email(db_session=db_session, email=update_request.email)

        if user_with_same_email:
            return UserResponse(status_code=400, success=False, message=f"Email '{update_request.email}' already exists")

    if db_user and db_user.id != update_request.id:
        return UserResponse(status_code=400, success=False, message="User id already exists")

    update_dict = update_request.dict(exclude_unset=True)

    # Process specific fields (exclude password from regular update)
    for key, value in update_dict.items():
        if value is not None and hasattr(db_user, key) and key != 'password':
            setattr(db_user, key, value)

    db_session.commit()
    db_session.refresh(db_user)
    return UserResponse(status_code=200, success=True, message="User successfully updated", user=db_user)


def delete_user(db_session: Session, user_id: int) -> UserResponse:
    existing_user = user_repository.find_active_user_by_id(db_session=db_session, user_id=user_id)

    if existing_user is None:
        return UserResponse(status_code=404, success=False, message="User does not exist")

    existing_user.entity_status = EntityStatus.DELETED
    existing_user.is_logged_in = False  # Ensure logged out when deleted
    db_session.delete(existing_user)
    db_session.commit()

    return UserResponse(status_code=201, success=True, message="User successfully deleted", user=existing_user)


def is_user_logged_in(db_session: Session, user_id: int) ->UserResponse:
    db_user = user_repository.find_active_user_by_id(db_session=db_session, user_id=user_id)
    if not db_user:
        return UserResponse(status_code=404, success=False, message=f"User with id {user_id} not found")

    if db_user.is_logged_in:
        return UserResponse(status_code=200, success=True, message="User is logged in", user=db_user)
    else:
        return UserResponse(status_code=401, success=False, message="User is not logged in")