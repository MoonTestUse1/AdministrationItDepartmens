"""Employee schemas"""
from pydantic import BaseModel
from datetime import datetime

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    department: str
    office: str

class EmployeeCreate(EmployeeBase):
    password: str

class Employee(EmployeeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 