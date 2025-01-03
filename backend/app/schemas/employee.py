"""Employee schemas"""
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    department: str
    office: str

    model_config = ConfigDict(from_attributes=True)

class EmployeeCreate(EmployeeBase):
    password: str

class EmployeeUpdate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True) 