"""Token model"""
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from ..database import Base

class Token(Base):
    """Token model"""
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    employee_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow) 