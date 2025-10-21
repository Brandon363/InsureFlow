from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from Config.database import SessionLocal


@asynccontextmanager
async def lifespan(app):
    db: Session = SessionLocal()
    try:
        print("This is where all the start up functions go")
        pass

    #     create_tender_source_request = TenderSourceCreateRequest(
    #         name='Tender Insight',
    #         code='TENDER_INSIGHT',
    #         base_url='www.insight.com',
    #         is_active=True,  # or False, depending on your default
    #         extraction_frequency=ExtractionFrequency.ON_DEMAND,  # or 'weekly', etc.
    #         extraction_method=ExtractionMethod.API,
    #         country='Zimbabwe'
    #     )
    #     etender_create_tender_source_request = TenderSourceCreateRequest(
    #         name='Etenders',
    #         code='ETENDERS',
    #         base_url='https://www.etenders.gov.za/',
    #         is_active=True,  # or False, depending on your default
    #         extraction_frequency=ExtractionFrequency.ON_DEMAND,  # or 'weekly', etc.
    #         extraction_method=ExtractionMethod.API,
    #         country='South Africa'
    #     )
    #     create_response = create_tender_source(create_tender_source_request, db)
    #     print(create_response.message)
    #     create_response = create_tender_source(etender_create_tender_source_request, db)
    #     print(create_response.message)
    #
    #     users: [UserCreateRequest] = [
    #         UserCreateRequest( first_name="Brandon", last_name="Mutombwa", other_initials="T", email="brandon.mutombwa@dataalafrica.com", password="123", username="brandon", user_role=UserRole.ADMIN),
    #         UserCreateRequest( first_name="Mary", last_name="Ann", other_initials="K", email="mary.ann@dataalafrica.com", password="123", username="maryann", user_role=UserRole.ADMIN),
    #         UserCreateRequest( first_name="Godfrey", last_name="Mbizo", email="godfrey.mbizo@dataalafrica.com", password="123", username="godfrey", user_role=UserRole.BUSINESS_DEV),
    #         UserCreateRequest( first_name="Trevor", last_name="Muchenje", email="trevor.muchenje@dataalafrica.com", password="123", username="trevor", user_role=UserRole.BUSINESS_DEV),
    #         UserCreateRequest( first_name="Medium", last_name="Musuta", email="medium.musuta@dataalafrica.com", password="123", username="medium", user_role=UserRole.BUSINESS_DEV),
    #     ]
    #
    #     for user in users:
    #         create_response = user_controller.create_user(user=user, db=db)
    #         print(create_response.message)

        yield
    finally:
        db.close()