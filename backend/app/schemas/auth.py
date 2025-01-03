"""Authentication schemas"""
from pydantic import BaseModel, ConfigDict

class AdminLogin(BaseModel):
    username: str
    password: str
    
    model_config = ConfigDict(from_attributes=True)

class EmployeeLogin(BaseModel):
    last_name: str
    password: str
    
    model_config = ConfigDict(from_attributes=True)

class EmployeeResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    department: str
    office: str
    access_token: str 

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    employee_id: int | None = None
    is_admin: bool = False

    model_config = ConfigDict(from_attributes=True) 