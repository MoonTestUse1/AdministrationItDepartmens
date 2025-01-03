"""Base class for SQLAlchemy models"""
from sqlalchemy.orm import declarative_base
from app.db.base_class import Base
from app.models.employee import Employee
from app.models.request import Request
from app.models.token import Token

Base = declarative_base()

# Импортируем все модели, чтобы Alembic мог их обнаружить
__all__ = ["Base", "Employee", "Request", "Token"] 