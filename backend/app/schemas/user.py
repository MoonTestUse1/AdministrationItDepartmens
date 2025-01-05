"""User schemas."""
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class UserBase(BaseModel):
    """User base schema."""
    model_config = ConfigDict(from_attributes=True)
    email: EmailStr
    full_name: str
    is_admin: bool = False

class UserCreate(UserBase):
    """User create schema."""
    password: str

class UserUpdate(BaseModel):
    """User update schema."""
    model_config = ConfigDict(from_attributes=True)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    """User schema."""
    id: int
    is_active: bool = True 