"""Chat schemas."""
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

class ChatFileBase(BaseModel):
    """Chat file base schema."""
    model_config = ConfigDict(from_attributes=True)
    filename: str
    file_path: str

class ChatFileCreate(ChatFileBase):
    """Chat file create schema."""
    message_id: int

class ChatFile(ChatFileBase):
    """Chat file schema."""
    id: int
    message_id: int
    created_at: datetime

class MessageBase(BaseModel):
    """Message base schema."""
    model_config = ConfigDict(from_attributes=True)
    content: str

class MessageCreate(MessageBase):
    """Message create schema."""
    chat_id: int

class Message(MessageBase):
    """Message schema."""
    id: int
    chat_id: int
    sender_id: int
    is_read: bool
    created_at: datetime
    files: List[ChatFile] = []

class ChatBase(BaseModel):
    """Chat base schema."""
    model_config = ConfigDict(from_attributes=True)
    employee_id: int

class ChatCreate(ChatBase):
    """Chat create schema."""
    pass

class Chat(ChatBase):
    """Chat schema."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    messages: List[Message] = [] 