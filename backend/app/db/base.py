"""Import all models for Alembic autogenerate support"""
from app.db.base_class import Base
from app.models.employee import Employee
from app.models.request import Request
from app.models.token import Token

# Импортируем все модели, чтобы Alembic мог их обнаружить
__all__ = ["Base", "Employee", "Request", "Token"] 