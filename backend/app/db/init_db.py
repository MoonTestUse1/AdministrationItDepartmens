"""Database initialization"""
from sqlalchemy.orm import Session
from ..models.employee import Employee
from ..utils.auth import get_password_hash

def init_db(db: Session) -> None:
    """Initialize database with default data"""
    # Проверяем, есть ли уже админ в базе
    admin = db.query(Employee).filter(Employee.is_admin == True).first()
    if not admin:
        # Создаем админа по умолчанию
        admin = Employee(
            first_name="Admin",
            last_name="User",
            department="IT",
            office="102",
            hashed_password=get_password_hash("adminpass123"),
            is_admin=True
        )
        db.add(admin)
        db.commit()
        db.refresh(admin) 