from datetime import datetime

from pydantic import BaseModel, Field, validator
from typing import Optional, List

from Schema.base_schema import BaseResponse
from Utils.Enums import EntityStatus


class AgentDTO(BaseModel):
    id: int = Field(description="This is the agent's id")
    first_name: str = Field(..., min_length=1)
    middle_name: Optional[str] = None
    last_name: str
    agent_number: str
    date_created: datetime
    date_updated: Optional[datetime]
    entity_status: EntityStatus

    class Config:
        from_attributes = True


class AgentCreateRequest(BaseModel):
    first_name: str = Field(..., min_length=1)
    middle_name: Optional[str] = None
    last_name: str
    password: str
    agent_number: str

    class Config:
        from_attributes = True


class AgentUpdateRequest(BaseModel):
    id: int = Field(description="This is the agent's id")
    first_name: Optional[str] = Field(..., min_length=1)
    middle_name: Optional[str] = None
    last_name: Optional[str]
    agent_number: str

    class Config:
        from_attributes = True


class AgentResponse(BaseResponse):
    agent: Optional[AgentDTO] = None
    agents: Optional[List[AgentDTO]] = None