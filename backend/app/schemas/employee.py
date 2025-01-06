"""Employee schemas"""
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    department: str
    office: str

    model_config = ConfigDict(from_attributes=True)

class EmployeeCreate(EmployeeBase):
    password: str

class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    department: Optional[str] = None
    office: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class Employee(EmployeeBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True) 