"""Request schemas"""
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from ..models.request import RequestStatus, RequestPriority

class RequestBase(BaseModel):
    department: str
    request_type: str
    description: str
    priority: RequestPriority

    model_config = ConfigDict(from_attributes=True)

class RequestCreate(RequestBase):
    pass

class RequestUpdate(BaseModel):
    status: RequestStatus

    model_config = ConfigDict(from_attributes=True)

class Request(RequestBase):
    id: int
    status: RequestStatus
    employee_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True) 