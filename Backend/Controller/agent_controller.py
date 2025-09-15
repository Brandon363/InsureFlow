from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from Config.database import get_db
from Schema.agent_schema import AgentResponse, AgentCreateRequest, AgentUpdateRequest
from Service import agent_service

router = APIRouter(
    prefix='/agent'
)


db_dependency = Annotated[Session, Depends(get_db)]

@router.post('/create-agent', response_model=AgentResponse)
def create_agent(create_request: AgentCreateRequest, db: db_dependency):
    return agent_service.create_agent(db_session=db, create_request=create_request)


@router.put('update-agent/{agent_id}', response_model=AgentResponse)
def update_agent(update_request: AgentUpdateRequest, agent_id: int, db: db_dependency):
    return agent_service.update_agent(db_session=db, update_request=update_request)

@router.get('get-all-active-agents', response_model=AgentResponse)
def get_all_active_agents(db: db_dependency):
    return agent_service.get_all_active_agents(db_session=db)


@router.get('get-active-agent-by-id/{agent_id}', response_model=AgentResponse)
def get_active_agent_by_id(agent_id: int, db: db_dependency):
    return agent_service.get_active_agent_by_id(db_session=db, agent_id=agent_id)


@router.get('get-active-agent-by-number/{agent_number}', response_model=AgentResponse)
def get_active_agent_by_number(agent_number: str, db: db_dependency):
    return agent_service.get_active_agent_by_agent_number(db_session=db, agent_number=agent_number)


@router.delete('delete-agent/{agent_id}', response_model=AgentResponse)
def delete_agent(agent_id: int, db: db_dependency) -> AgentResponse:
    return agent_service.delete_agent(db_session=db,agent_id=agent_id)