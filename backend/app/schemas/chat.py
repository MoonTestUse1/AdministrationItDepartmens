from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.schemas.user import User

class ChatFileBase(BaseModel):
    file_name: str
    file_size: int

class ChatFileCreate(ChatFileBase):
    pass

class ChatFile(ChatFileBase):
    id: int
    message_id: int
    file_path: str
    created_at: datetime

    class Config:
        from_attributes = True

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    chat_id: int
    sender_id: int
    is_read: bool
    created_at: datetime
    files: List[ChatFile] = []

    class Config:
        from_attributes = True

class ChatBase(BaseModel):
    employee_id: int
    admin_id: int

class ChatCreate(ChatBase):
    pass

class Chat(ChatBase):
    id: int
    created_at: datetime
    employee: User
    admin: User
    last_message: Optional[Message] = None
    unread_count: Optional[int] = 0

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