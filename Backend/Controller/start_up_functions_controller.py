from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from Config.database import SessionLocal
from Service import UserService
from Utils.seed_users import users_to_seed


@asynccontextmanager
async def lifespan(app):
    db: Session = SessionLocal()
    try:
        for user in users_to_seed:
            create_response = UserService.create_user(create_request=user, db_session=db)
            print(f"{user.first_name} {user.last_name}: {create_response.message}")
        yield
    finally:
        db.close()
