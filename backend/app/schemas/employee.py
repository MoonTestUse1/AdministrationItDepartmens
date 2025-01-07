"""Employee schemas"""
from typing import Optional
from pydantic import BaseModel, EmailStr

class EmployeeBase(BaseModel):
    """Base employee schema"""
    login: str
    first_name: str
    last_name: str
    department: str
    office: str
    is_active: bool = True
    is_admin: bool = False

class EmployeeCreate(EmployeeBase):
    """Employee creation schema"""
    password: str
    hashed_password: Optional[str] = None

class EmployeeUpdate(BaseModel):
    """Employee update schema"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    department: Optional[str] = None
    office: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None

class Employee(EmployeeBase):
    """Employee schema"""
    id: int

    class Config:
        """Pydantic config"""
        from_attributes = True 