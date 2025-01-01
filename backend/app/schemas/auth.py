"""Authentication schemas"""
from pydantic import BaseModel

class AdminLogin(BaseModel):
    username: str
    password: str

class EmployeeLogin(BaseModel):
    last_name: str
    password: str 