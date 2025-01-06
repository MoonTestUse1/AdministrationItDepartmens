"""Employee schemas"""
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional

class EmployeeBase(BaseModel):
    email: EmailStr
    full_name: str
    department: Optional[str] = None
    is_active: bool = True
    is_admin: bool = False

    model_config = ConfigDict(from_attributes=True)

class EmployeeCreate(EmployeeBase):
    password: str

class EmployeeUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    department: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)

class Employee(EmployeeBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True) 