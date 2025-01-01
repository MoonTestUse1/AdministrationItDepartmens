"""Models initialization"""
from ..database import Base, engine
from .employee import Employee
from .request import Request

# Create all tables
Base.metadata.create_all(bind=engine) 