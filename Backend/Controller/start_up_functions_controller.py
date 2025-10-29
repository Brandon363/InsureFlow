from contextlib import asynccontextmanager
from datetime import date

from sqlalchemy.orm import Session
from Config.database import SessionLocal
from Model.UserModel import UserCreateRequest

from Service import UserService
from Utils.Enums import UserRole


@asynccontextmanager
async def lifespan(app):
    db: Session = SessionLocal()
    try:
        users: [UserCreateRequest] = [UserCreateRequest(
            id_number="75-191961 R 00",
            email="andrew@gmail.com",
            first_name="ANDREW",
            last_name="ROBERTS",
            other_names="WILLIAM L",
            user_role=UserRole.ADMIN,
            date_of_birth=date(1959, 11, 17),
            village_of_origin="",
            place_of_birth="HARARE",
            phone_number=None,
            address=None,
            password="passworddd"
        ),
            UserCreateRequest(
                id_number="63-758552 Y 27",
                email="mutumwa@gmail.com",  # Email not available on the ID card
                first_name="MUTUMWA",
                last_name="DZIVA",
                other_names="MAWER",
                user_role=UserRole.CUSTOMER,
                date_of_birth=date(1960, 11, 1),
                village_of_origin="BINDUR",
                place_of_birth="MAWERE",
                phone_number=None,  # Phone number not available on the ID card
                address=None,  # Address not available on the ID card
                password="passworddd"  # Password would need to be set separately
            ),
            UserCreateRequest(
                id_number="45-190221 E 45",
                email="expetrollcapolator@gmail.com",  # email not available in the image
                first_name="EXPETROLLCAPOLATOR",
                last_name="CHIMUNDEGE",
                other_names=None,
                user_role=UserRole.CUSTOMER,  # user_role not available in the image
                date_of_birth=date(1994, 4, 3),
                village_of_origin="KAJOKOTO",
                place_of_birth="MOUNT DARWIN",
                phone_number=None,  # phone_number not available in the image
                address=None,  # address not available in the image
                password="passworddd"  # password not available in the image
            )
        ]
        for user in users:
            create_response = UserService.create_user(
                create_request=user, db_session=db)
            print(create_response.message)

        yield
    finally:
        db.close()
