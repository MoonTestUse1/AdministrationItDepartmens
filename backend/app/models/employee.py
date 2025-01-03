"""Employee model"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..db.base import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    department = Column(String)
    office = Column(String)
    hashed_password = Column(String)

    # Определяем отношение к Request
    requests = relationship(
        "Request",
        back_populates="employee",
        cascade="all, delete-orphan"
    )