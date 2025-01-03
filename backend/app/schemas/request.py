"""Request schemas"""
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict
from typing import Optional

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
    status: RequestStatus = RequestStatus.NEW

class RequestCreate(RequestBase):
    pass

class RequestUpdate(BaseModel):
    status: RequestStatus
    
    model_config = ConfigDict(from_attributes=True)

class Request(RequestBase):
    id: int
    employee_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class RequestStatistics(BaseModel):
    total: int
    new: int
    in_progress: int
    completed: int
    rejected: int
    
    model_config = ConfigDict(from_attributes=True) 