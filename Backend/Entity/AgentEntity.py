from datetime import datetime

from Config.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum

from Utils.Enums import EntityStatus


class AgentEntity(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    first_name = Column(String(255), nullable=False)
    middle_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=False)
    agent_number = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)

    date_created = Column(DateTime, default=datetime.utcnow, nullable=True)
    date_updated = Column(DateTime, onupdate=datetime.utcnow, nullable=True)
    entity_status = Column(SQLEnum(EntityStatus), nullable=False, default=EntityStatus.ACTIVE)