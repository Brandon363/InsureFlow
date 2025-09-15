from fastapi import FastAPI, APIRouter
from Config.database import Base, engine
from Config.middleware_and_cors import MyMiddleware
from starlette.middleware.cors import CORSMiddleware
from Controller import agent_controller

# import tables so that they are created
from Entity.AgentEntity import AgentEntity

# create the tables if they don't exist
Base.metadata.create_all(bind=engine)



app = FastAPI(
    title="Insure Flow API",
    version="1.0.0"
)

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(agent_controller.router, tags=["Agents"])

@api_router.get("/")
def read_root():
    return {"Server is running"}


app.include_router(api_router)


app.add_middleware(MyMiddleware)
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_methods=["*"],
                   allow_headers=["*"],
                   allow_credentials=True)
