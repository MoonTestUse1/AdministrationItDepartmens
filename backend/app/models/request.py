"""Request model"""
from .base import Base, Column, Integer, String, DateTime, ForeignKey, Enum, func, relationship
import enum

class RequestStatus(str, enum.Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

class RequestPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Request(Base):
    __tablename__ = "requests"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    department = Column(String, nullable=False)
    request_type = Column(String, nullable=False)
    priority = Column(Enum(RequestPriority), nullable=False)
    description = Column(String, nullable=False)
    status = Column(Enum(RequestStatus), nullable=False, default=RequestStatus.NEW)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    employee = relationship("Employee", back_populates="requests")
