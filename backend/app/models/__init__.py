"""Models package"""
from .employee import Employee
from .request import Request, RequestStatus, RequestPriority

# Регистрируем модели в правильном порядке
Employee.requests  # Инициализируем отношение
Request.employee  # Инициализируем отношение

__all__ = ['Employee', 'Request', 'RequestStatus', 'RequestPriority'] 