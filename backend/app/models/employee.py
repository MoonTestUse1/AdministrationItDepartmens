"""Employee models"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class EmployeeBase(BaseModel):
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    department: str = Field(..., pattern="^(aho|gkh|general)$")
    office: str = Field(..., min_length=1)

class EmployeeCreate(EmployeeBase):
    password: str = Field(..., min_length=6)

class Employee(EmployeeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True