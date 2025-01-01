"""Employee model"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Employee(Base):
    __tablename__ = "employees"
    __table_args__ = {'extend_existing': True}
    __module__ = "app.models.employee"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    department = Column(String, nullable=False)
    office = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    requests = relationship("Request", back_populates="employee", lazy="dynamic")