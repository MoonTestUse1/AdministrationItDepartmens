"""Token schemas"""
from pydantic import BaseModel, ConfigDict

class Token(BaseModel):
    access_token: str
    token_type: str

    model_config = ConfigDict(from_attributes=True)

class TokenData(BaseModel):
    employee_id: int | None = None

    model_config = ConfigDict(from_attributes=True) 