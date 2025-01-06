"""Models initialization"""
from ..database import Base, engine
from .employee import Employee
from .request import Request
from .token import Token

# Создаем все таблицы
Base.metadata.create_all(bind=engine)

__all__ = ['Base', 'Employee', 'Request', 'Token'] 