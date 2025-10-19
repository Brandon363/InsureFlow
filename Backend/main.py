from fastapi import FastAPI, APIRouter, HTTPException
from Config.database import Base, engine
from Config.middleware_and_cors import MyMiddleware
from starlette.middleware.cors import CORSMiddleware
from Controller import agent_controller, user_controller, policy_controller, claim_controller, document_controller, \
    payment_controller, notification_controller
from fastapi.responses import JSONResponse

# import tables so that they are created
from Entity.UserEntity import UserEntity
from Entity.AgentEntity import AgentEntity
from Entity.ClaimEntity import ClaimEntity
from Entity.DocumentEntity import DocumentEntity
from Entity.NotificationEntity import NotificationEntity
from Entity.PaymentEntity import PaymentEntity
from Entity.PolicyEntity import PolicyEntity

# create the tables if they don't exist
Base.metadata.create_all(bind=engine)




app = FastAPI(
    title="Insure Flow API",
    version="1.0.0"
)

api_router = APIRouter(prefix="/api/v1")
app.include_router(payment_controller.router, tags=["Payments"])
app.include_router(notification_controller.router, tags=["Notifications"])
api_router.include_router(document_controller.router, tags=["Documents"])
api_router.include_router(claim_controller.router, tags=["Claims"])
api_router.include_router(policy_controller.router, tags=["Policies"])
api_router.include_router(user_controller.router, tags=["Users"])
api_router.include_router(agent_controller.router, tags=["Agents"])

@api_router.get("/")
def read_root():
    return {"Server is running"}


@api_router.delete("/delete-all-tables")
def delete_all_tables():
    try:
        Base.metadata.drop_all(engine)
        return JSONResponse(content={"message": "All tables deleted successfully", "status": "success"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": f"Failed to delete tables: {str(e)}", "status": "failed"}, status_code=500)

@api_router.post("create-all-tables")
def create_all_tables():
    try:
        Base.metadata.create_all(engine)
        return JSONResponse(content={"message": "All tables created successfully", "status": "success"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": f"Failed to create tables: {str(e)}", "status": "failed"}, status_code=500)



app.include_router(api_router)


app.add_middleware(MyMiddleware)
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_methods=["*"],
                   allow_headers=["*"],
                   allow_credentials=True)
