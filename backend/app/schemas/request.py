"""Request schemas"""
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class RequestStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

class RequestPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class RequestBase(BaseModel):
    department: str
    request_type: str
    priority: RequestPriority
    description: str

class RequestCreate(RequestBase):
    employee_id: int

class Request(RequestBase):
    id: int
    status: RequestStatus
    created_at: datetime
    employee_id: int

    class Config:
        from_attributes = True

class RequestWithEmployee(Request):
    employee_last_name: str
    employee_first_name: str

    class Config:
        from_attributes = True 