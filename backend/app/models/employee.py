"""Employee model"""
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from ..db.base_class import Base

class Employee(Base):
    """Employee model"""
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    department = Column(String, nullable=False)
    office = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    # Отношения
    requests = relationship("Request", back_populates="employee", cascade="all, delete-orphan")
    tokens = relationship("Token", back_populates="employee", cascade="all, delete-orphan")