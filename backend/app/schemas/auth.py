"""Authentication schemas"""
from pydantic import BaseModel

class AdminLogin(BaseModel):
    username: str
    password: str

class EmployeeLogin(BaseModel):
    last_name: str
    password: str

class EmployeeResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    department: str
    office: str
    access_token: str 