

from sqlalchemy.orm import Session

from Entity.AgentEntity import AgentEntity
from Utils.Enums import EntityStatus


def find_active_agent_by_id(db_session:Session, agent_id: int):
    return db_session.query(AgentEntity).filter(
        AgentEntity.id == agent_id, AgentEntity.entity_status == EntityStatus.ACTIVE).first()


def find_all_active_active_agents(db_session: Session):
    return db_session.query(AgentEntity).filter(AgentEntity.entity_status == EntityStatus.ACTIVE).all()


def find_active_agent_by_agent_number(db_session:Session, agent_number: str):
    return db_session.query(AgentEntity).filter(
        AgentEntity.agent_number == agent_number, AgentEntity.entity_status == EntityStatus.ACTIVE).first()