"""Employee schemas"""
from pydantic import BaseModel, ConfigDict

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    department: str
    office: str
    
    model_config = ConfigDict(from_attributes=True)

class EmployeeCreate(EmployeeBase):
    password: str

class EmployeeUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    department: str | None = None
    office: str | None = None
    
    model_config = ConfigDict(from_attributes=True)

class EmployeeResponse(EmployeeBase):
    id: int 