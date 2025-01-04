from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    # Отношения для чата
    employee_chats = relationship("Chat", foreign_keys="[Chat.employee_id]", back_populates="employee")
    admin_chats = relationship("Chat", foreign_keys="[Chat.admin_id]", back_populates="admin")
    sent_messages = relationship("Message", back_populates="sender")
    
    # Отношения для заявок
    requests = relationship("Request", back_populates="employee") 