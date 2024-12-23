from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from models import RequestStatus


class EmployeeBase(BaseModel):
    last_name: str
    first_name: str
    department: str
    office: str


class EmployeeCreate(EmployeeBase):
    password: str


class Employee(EmployeeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class RequestBase(BaseModel):
    department: str
    request_type: str
    priority: str
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
