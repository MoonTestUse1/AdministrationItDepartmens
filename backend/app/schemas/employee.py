"""Employee schemas"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EmployeeBase(BaseModel):
    """Base employee schema"""
    first_name: str
    last_name: str
    department: str
    office: str
    is_admin: bool = False

class EmployeeCreate(EmployeeBase):
    """Employee creation schema"""
    password: str

class EmployeeUpdate(BaseModel):
    """Employee update schema"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    department: Optional[str] = None
    office: Optional[str] = None

class Employee(EmployeeBase):
    """Employee schema"""
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        """Pydantic config"""
        from_attributes = True 