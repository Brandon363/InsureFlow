from fastapi import FastAPI, APIRouter, HTTPException
from Config.database import Base, engine
from Config.middleware_and_cors import MyMiddleware
from starlette.middleware.cors import CORSMiddleware
from Controller import agent_controller, user_controller, policy_controller, claim_controller, document_controller, \
    payment_controller, notification_controller, ExtractedUserController, TemporaryLossApplicationController, \
    DependentController, ApplicationTrackingController, ExtractedTemporaryLossApplicationController, \
    ExtractedDependentsController, VerificationTrackingController, FreeTextController
from fastapi.responses import JSONResponse
from Controller.start_up_functions_controller import lifespan
from sqlalchemy import MetaData, text

# import tables so that they are created
from Entity.UserEntity import UserEntity
from Entity.AgentEntity import AgentEntity
from Entity.ClaimEntity import ClaimEntity
from Entity.DocumentEntity import DocumentEntity
from Entity.NotificationEntity import NotificationEntity
from Entity.PaymentEntity import PaymentEntity
from Entity.PolicyEntity import PolicyEntity
from Entity.ExtractedUserEntity import ExtractedUserEntity
from Entity.ApplicationTrackingEntity import ApplicationTrackingEntity
from Entity.DependentEntity import DependentEntity
from Entity.ExtractedDependentEntity import ExtractedDependentEntity
from Entity.ExtractedTemporaryLossApplicationEntity import ExtractedTemporaryLossApplicationEntity
from Entity.VerificationTrackingEntity import VerificationTrackingEntity
from Entity.TemporaryLossApplicationEntity import TemporaryLossApplicationEntity

# create the tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Insure Flow API",
    version="1.0.0",
    lifespan=lifespan
)

# api_router = APIRouter(prefix="/api/v1")
api_router = APIRouter()
app.include_router(ExtractedTemporaryLossApplicationController.router, tags=["Extracted Temporary Loss Applications"])
app.include_router(ExtractedDependentsController.router, tags=["Extracted Dependents"])
app.include_router(DependentController.router, tags=["Dependents"])
app.include_router(payment_controller.router, tags=["Payments"])
app.include_router(notification_controller.router, tags=["Notifications"])
api_router.include_router(document_controller.router, tags=["Documents"])
api_router.include_router(claim_controller.router, tags=["Claims"])
api_router.include_router(policy_controller.router, tags=["Policies"])
api_router.include_router(user_controller.router, tags=["Users"])
api_router.include_router(ExtractedUserController.router, tags=["Extracted Users"])
api_router.include_router(FreeTextController.router, tags=["Free Text"])
api_router.include_router(agent_controller.router, tags=["Agents"])
api_router.include_router(TemporaryLossApplicationController.router, tags=["Temporary Loss Application"])
api_router.include_router(ApplicationTrackingController.router, tags=["Application Tracking"])
api_router.include_router(VerificationTrackingController.router, tags=["Verification Tracking"])


@api_router.get("/")
def read_root():
    return {"Server is running"}


#
# @app.post("/recreate-tables/")
# def recreate_tables_endpoint():
#     try:
#         # Drop all tables
#         Base.metadata.drop_all(engine)
#         # Create all tables
#         Base.metadata.create_all(engine)
#         return {"message": "Tables recreated successfully"}
#     except Exception as e:
#         return {"message": f"Error recreating tables: {str(e)}"}

@app.post("/recreate-tables/")
def recreate_tables_endpoint():
    try:
        meta = MetaData()
        meta.reflect(bind=engine)

        with engine.connect() as conn:
            # Disable all constraints first
            for table in reversed(meta.sorted_tables):
                conn.execute(text(f"ALTER TABLE {table.name} NOCHECK CONSTRAINT ALL"))

            # Drop all tables
            Base.metadata.drop_all(bind=engine)

            # Recreate all tables
            Base.metadata.create_all(bind=engine)

        return {"message": "Tables recreated successfully"}

    except Exception as e:
        return {"message": f"Error recreating tables: {str(e)}"}



#


@api_router.delete("/delete-all-tables")
def delete_all_tables():
    try:
        Base.metadata.drop_all(engine)
        return JSONResponse(content={"message": "All tables deleted successfully", "status": "success"},
                            status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": f"Failed to delete tables: {str(e)}", "status": "failed"},
                            status_code=500)


@api_router.post("create-all-tables")
def create_all_tables():
    try:
        Base.metadata.create_all(engine)
        return JSONResponse(content={"message": "All tables created successfully", "status": "success"},
                            status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": f"Failed to create tables: {str(e)}", "status": "failed"},
                            status_code=500)


app.include_router(api_router)

app.add_middleware(MyMiddleware)
app.add_middleware(CORSMiddleware,
                   allow_origins=["http://10.147.16.251:4200", "http://localhost:4200"],
                   allow_methods=["*"],
                   allow_headers=["*"],
                   allow_credentials=True)
