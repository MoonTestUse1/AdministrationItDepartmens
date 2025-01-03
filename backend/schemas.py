"""Schemas for the application"""
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from models import RequestStatus

class Token(BaseModel):
    access_token: str
    token_type: str

    model_config = ConfigDict(from_attributes=True)

class TokenData(BaseModel):
    user_id: int | None = None

    model_config = ConfigDict(from_attributes=True)

class EmployeeBase(BaseModel):
    last_name: str
    first_name: str
    department: str
    office: str

    model_config = ConfigDict(from_attributes=True)

class EmployeeCreate(EmployeeBase):
    password: str

class Employee(EmployeeBase):
    id: int
    created_at: datetime

class RequestBase(BaseModel):
    department: str
    request_type: str
    priority: str
    description: str

    model_config = ConfigDict(from_attributes=True)

class RequestCreate(RequestBase):
    employee_id: int

class Request(RequestBase):
    id: int
    status: RequestStatus
    created_at: datetime
    employee_id: int
