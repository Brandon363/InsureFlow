from datetime import datetime
from pydantic import BaseModel, Field, validator, ConfigDict
from typing import Optional, List
from Model.ResponseModel import BaseResponse
from Utils.Enums import EntityStatus


class AgentDTO(BaseModel):
    id: int = Field(description="This is the agent's id")
    user_id: int
    agent_number: str
    date_created: datetime
    date_updated: Optional[datetime]
    entity_status: EntityStatus

    model_config = ConfigDict(from_attributes=True)


class AgentCreateRequest(BaseModel):
    user_id: int
    agent_number: str
    model_config = ConfigDict(from_attributes=True)


class AgentUpdateRequest(BaseModel):
    # Remove id field since it comes from URL path in agent_controller
    # id: int = Field(description="This is the agent's id")
    user_id: int
    agent_number: str
    model_config = ConfigDict(from_attributes=True)


class AgentResponse(BaseResponse):
    agent: Optional[AgentDTO] = None
    agents: Optional[List[AgentDTO]] = None