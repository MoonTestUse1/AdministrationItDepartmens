"""Database initialization script"""
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.employee import Employee
from app.utils.auth import get_password_hash

def init_db(db: Session) -> None:
    """Initialize database with default data"""
    # Создаем администратора по умолчанию
    admin = db.query(Employee).filter(Employee.email == settings.ADMIN_USERNAME).first()
    if not admin:
        admin = Employee(
            email=settings.ADMIN_USERNAME,
            full_name="System Administrator",
            hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
            is_active=True,
            is_admin=True,
            department="Administration"
        )
        db.add(admin)
        db.commit()
        db.refresh(admin) 