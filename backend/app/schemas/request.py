"""Request schemas"""
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class RequestBase(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    request_type: str
    description: str
    priority: str

class RequestCreate(RequestBase):
    pass

class RequestUpdate(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    status: str

class Request(RequestBase):
    id: int
    employee_id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 