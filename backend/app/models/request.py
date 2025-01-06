"""Request model"""
from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SQLEnum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from ..database import Base

class RequestStatus(str, Enum):
    """Request status enum"""
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"

class RequestPriority(str, Enum):
    """Request priority enum"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class RequestType(str, Enum):
    """Request type enum"""
    VACATION = "vacation"
    SICK_LEAVE = "sick_leave"
    EQUIPMENT = "equipment"
    OTHER = "other"

class Request(Base):
    """Request model"""
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    request_type = Column(SQLEnum(RequestType), nullable=False)
    description = Column(String, nullable=False)
    priority = Column(SQLEnum(RequestPriority), nullable=False, default=RequestPriority.MEDIUM)
    status = Column(SQLEnum(RequestStatus), nullable=False, default=RequestStatus.NEW)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)

    employee = relationship("Employee", back_populates="requests")
