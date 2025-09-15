from enum import Enum

class EntityStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DELETED = "delete"