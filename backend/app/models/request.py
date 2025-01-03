"""Request model"""
from enum import Enum
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class RequestStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"

class RequestPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    department = Column(String, index=True)
    request_type = Column(String, index=True)
    description = Column(String)
    priority = Column(String)
    status = Column(String, default=RequestStatus.NEW)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Определяем отношение к Employee
    employee = relationship("Employee", back_populates="requests")
