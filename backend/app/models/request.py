"""Request model"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base
import enum

class RequestStatus(str, enum.Enum):
    new = "new"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"

class RequestPriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class Request(Base):
    __tablename__ = "requests"
    __table_args__ = {'extend_existing': True}
    __module__ = "app.models.request"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    department = Column(String, nullable=False)
    request_type = Column(String, nullable=False)
    priority = Column(Enum(RequestPriority), nullable=False)
    description = Column(String, nullable=False)
    status = Column(Enum(RequestStatus), default=RequestStatus.new)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    employee = relationship("Employee", back_populates="requests")
