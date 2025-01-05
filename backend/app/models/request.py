"""Request model."""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
from app.schemas.request import RequestPriority, RequestStatus

class Request(Base):
    """Request model."""
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    request_type = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(Enum(RequestPriority), nullable=False)
    status = Column(Enum(RequestStatus), default=RequestStatus.NEW)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Отношения
    employee = relationship("Employee", back_populates="requests")
