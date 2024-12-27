from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String, index=True)
    # другие поля...

    requests = relationship("Request", back_populates="employee")


class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    # другие поля...

    employee = relationship("Employee", back_populates="requests")
