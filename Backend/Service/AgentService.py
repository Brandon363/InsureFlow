from sqlalchemy.orm import Session
from Entity.AgentEntity import AgentEntity
from Repository import agent_repository, user_repository
from Model.AgentModel import AgentResponse, AgentCreateRequest, AgentUpdateRequest
from Utils.Enums import EntityStatus


def get_active_agent_by_id(db_session: Session, agent_id: int) -> AgentResponse:
    # validate if number
    if agent_id is None:
        return AgentResponse(status_code=400, success=False, message="Agent ID cannot be null")

    # get agent from database
    db_agent = agent_repository.find_active_agent_by_id(db_session=db_session, agent_id=agent_id)
    if db_agent is None:
        return AgentResponse(status_code=404, success=False, message=f"Agent with id {agent_id} not found")

    return AgentResponse(status_code=200, success=True, message="Agent successfully found", agent=db_agent)


def get_active_agent_by_agent_number(db_session: Session, agent_number: str) -> AgentResponse:
    # validate if number
    if agent_number is None:
        return AgentResponse(status_code=400, success=False, message="Agent number cannot be null")

    # get agent from database
    db_agent = agent_repository.find_active_agent_by_agent_number(db_session=db_session, agent_number=agent_number)
    if db_agent is None:
        return AgentResponse(status_code=404, success=False, message=f"Agent with number {agent_number} not found")

    return AgentResponse(status_code=200, success=True, message="Agent successfully found", agent=db_agent)


def get_all_active_agents(db_session:Session)-> AgentResponse:
    db_agents = agent_repository.find_all_active_active_agents(db_session=db_session)

    if db_agents is None:
        return AgentResponse(status_code=404, success=False, message=f"Agents not found")

    return AgentResponse(status_code=200, success=True, message="Agents successfully found", agents=db_agents)



def create_agent(db_session: Session, create_request: AgentCreateRequest) -> AgentResponse:
    # Validate if user exists before creating the agent
    existing_user = user_repository.find_active_user_by_id(db_session=db_session, user_id=create_request.user_id)

    if not existing_user:
        return AgentResponse(status_code= 404, success=False, message=f"User with id {create_request.user_id} does not exist")

    # see if agent number exists
    db_agent_response = get_active_agent_by_agent_number(db_session=db_session, agent_number=create_request.agent_number)

    if db_agent_response.success:
        return AgentResponse(status_code=400, success=False, message="Agent number already exists")

    agent_entity: AgentEntity = AgentEntity(**create_request.dict())
    db_session.add(agent_entity)
    db_session.commit()
    db_session.refresh(agent_entity)

    return AgentResponse(status_code=201, success=True, message="Agent created successfully", agent=agent_entity)


def update_agent(db_session:Session, agent_id:int, update_request: AgentUpdateRequest) -> AgentResponse:
    # Find the agent by ID to ensure it exists
    existing_agent = agent_repository.find_active_agent_by_id(db_session=db_session, agent_id=agent_id)

    if not existing_agent:
        return AgentResponse(status_code=404, success=False, message=f"Agent with id {agent_id} not found")

    # Check if agent number is being changed anf if it conflicts with another agent
    if update_request.agent_number != existing_agent.agent_number:
        agent_with_the_same_number = agent_repository.find_active_agent_by_agent_number(db_session=db_session, agent_number=update_request.agent_number)

        if agent_with_the_same_number:
            return AgentResponse(status_code=400, success=False, message=f"Agent number '{update_request.agent_number}' already exists")

    # Convert update data to dict (exclude unset fields)
    update_dict = update_request.dict(exclude_unset=True)

    # Process specific fields
    for key, value in update_dict.items():
        if value is not None and hasattr(existing_agent, key):
            setattr(existing_agent, key, value)

    db_session.commit()
    db_session.refresh(existing_agent)
    return AgentResponse(status_code=200, success=True, message="Agent updated successfully", agent=existing_agent)


def delete_agent(db_session: Session, agent_id: int) -> AgentResponse:
    # Find existing agent
    existing_agent = agent_repository.find_active_agent_by_id(db_session, agent_id)

    # Check if the agent exists
    if existing_agent is None:
        return AgentResponse(status_code=404, message="Agent not found", success=False)

    existing_agent.entity_status = EntityStatus.DELETED

    # Save changes
    db_session.commit()
    db_session.refresh(existing_agent)

    return AgentResponse(status_code=201, message="Agent successfully deleted", success=True, agent=existing_agent)

