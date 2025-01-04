"""Request models"""
from enum import Enum
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..db.base import Base


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


class Request(Base):
    """Request model"""
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    status = Column(SQLAlchemyEnum(RequestStatus), nullable=False, default=RequestStatus.NEW)
    priority = Column(SQLAlchemyEnum(RequestPriority), nullable=False)
    request_type = Column(String, nullable=False)
    department = Column(String, nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Определяем отношение к Employee
    employee = relationship("Employee", back_populates="requests")
