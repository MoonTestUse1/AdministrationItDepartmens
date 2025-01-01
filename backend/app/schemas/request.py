"""Request schemas"""
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict

class RequestStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"

class RequestPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class RequestBase(BaseModel):
    title: str
    description: str
    priority: RequestPriority
    
    model_config = ConfigDict(from_attributes=True)

class RequestCreate(RequestBase):
    pass

class RequestUpdate(BaseModel):
    status: RequestStatus
    
    model_config = ConfigDict(from_attributes=True)

class RequestResponse(RequestBase):
    id: int
    status: RequestStatus
    created_at: datetime
    employee_id: int

class RequestStatistics(BaseModel):
    total: int
    new: int
    in_progress: int
    completed: int
    rejected: int
    
    model_config = ConfigDict(from_attributes=True) 