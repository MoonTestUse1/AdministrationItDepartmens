"""Request schemas."""
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from enum import Enum

class RequestPriority(str, Enum):
    """Request priority enum."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class RequestStatus(str, Enum):
    """Request status enum."""
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"

class RequestBase(BaseModel):
    """Request base schema."""
    model_config = ConfigDict(from_attributes=True)
    request_type: str
    description: str
    priority: RequestPriority

class RequestCreate(RequestBase):
    """Request create schema."""
    pass

class RequestUpdate(BaseModel):
    """Request update schema."""
    model_config = ConfigDict(from_attributes=True)
    status: RequestStatus

class Request(RequestBase):
    """Request schema."""
    id: int
    employee_id: int
    status: RequestStatus
    created_at: datetime
    updated_at: Optional[datetime] = None 