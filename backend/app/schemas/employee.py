"""Employee schemas"""
from pydantic import BaseModel, ConfigDict
from typing import Optional

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    department: str
    office: str

class EmployeeCreate(EmployeeBase):
    password: str

class EmployeeUpdate(EmployeeBase):
    password: Optional[str] = None

class Employee(EmployeeBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    hashed_password: str 