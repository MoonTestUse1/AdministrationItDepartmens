"""Request schemas"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from ..models.request import RequestStatus, RequestPriority

class RequestBase(BaseModel):
    employee_id: int
    department: str
    request_type: str
    priority: RequestPriority
    description: str

class RequestCreate(RequestBase):
    pass

class RequestResponse(RequestBase):
    id: int
    status: RequestStatus
    created_at: datetime

    class Config:
        from_attributes = True 