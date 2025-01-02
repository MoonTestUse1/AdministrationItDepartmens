"""Request schemas"""
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict
from typing import Optional

class RequestStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

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
    employee_id: int

class Request(RequestBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    employee_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class RequestUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    status: RequestStatus 