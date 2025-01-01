"""Table schemas"""
from pydantic import BaseModel, ConfigDict

class TableBase(BaseModel):
    name: str
    description: str
    
    model_config = ConfigDict(from_attributes=True)

class TableCreate(TableBase):
    pass

class TableResponse(TableBase):
    id: int
