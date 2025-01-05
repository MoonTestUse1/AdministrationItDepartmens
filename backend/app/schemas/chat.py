"""Chat schemas"""
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from app.models.user import User

class ChatBase(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    employee_id: int

class ChatCreate(ChatBase):
    pass

class MessageBase(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    content: str
    chat_id: int
    sender_id: int

class MessageCreate(MessageBase):
    pass

class ChatFileBase(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    filename: str
    file_path: str
    message_id: int

class ChatFileCreate(ChatFileBase):
    pass

class ChatFile(ChatFileBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Message(MessageBase):
    id: int
    is_read: bool
    created_at: datetime
    files: List[ChatFile] = []

    class Config:
        from_attributes = True

class Chat(ChatBase):
    id: int
    employee: User
    messages: List[Message] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Схемы для WebSocket сообщений
class WSMessage(BaseModel):
    type: str
    content: Optional[str] = None
    message_ids: Optional[List[int]] = None
    files: Optional[List[dict]] = None

class WSResponse(BaseModel):
    type: str
    id: Optional[int] = None
    sender_id: Optional[int] = None
    content: Optional[str] = None
    created_at: Optional[datetime] = None
    is_read: Optional[bool] = None
    message_ids: Optional[List[int]] = None
    files: Optional[List[ChatFile]] = None
    error: Optional[str] = None 