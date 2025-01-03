"""Token model"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from ..db.base import Base

class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    user_id = Column(Integer, index=True)  # -1 для админа, остальные для сотрудников
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 