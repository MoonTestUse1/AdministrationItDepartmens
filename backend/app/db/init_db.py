"""Database initialization script"""
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.employee import Employee
from app.utils.auth import get_password_hash

def init_db(db: Session) -> None:
    """Initialize database with default data"""
    # Создаем тестового сотрудника
    test_employee = db.query(Employee).filter(Employee.last_name == "User").first()
    if not test_employee:
        test_employee = Employee(
            first_name="Test",
            last_name="User",
            department="IT",
            office="101",
            hashed_password=get_password_hash("testpass123")
        )
        db.add(test_employee)
        db.commit()
        db.refresh(test_employee) 