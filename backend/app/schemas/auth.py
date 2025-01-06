"""Authentication schemas"""
from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    """Token schema"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Token data schema"""
    employee_id: Optional[int] = None
    is_admin: bool = False

class LoginCredentials(BaseModel):
    """Login credentials schema"""
    username: str  # В формате "Имя Фамилия"
    password: str 