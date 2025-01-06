"""Request schemas"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from ..models.request import RequestStatus, RequestPriority, RequestType

class RequestBase(BaseModel):
    """Base request schema"""
    request_type: RequestType
    description: str
    priority: RequestPriority = RequestPriority.MEDIUM

class RequestCreate(RequestBase):
    """Request create schema"""
    pass

class Request(RequestBase):
    """Request schema"""
    id: int
    status: RequestStatus
    created_at: datetime
    employee_id: int

    class Config:
        """Pydantic config"""
        from_attributes = True

class RequestUpdate(BaseModel):
    """Request update schema"""
    status: RequestStatus 