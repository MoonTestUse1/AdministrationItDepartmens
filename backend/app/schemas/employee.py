"""Employee schemas"""
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class EmployeeBase(BaseModel):
    email: str
    full_name: str
    department: str
    is_active: bool = True
    is_admin: bool = False

    model_config = ConfigDict(from_attributes=True)

class EmployeeCreate(EmployeeBase):
    password: str

class EmployeeUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    department: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)

class Employee(EmployeeBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True) 