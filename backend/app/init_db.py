"""Database initialization"""
from .database import Base, engine
from .models.employee import Employee
from .models.request import Request, RequestStatus, RequestPriority

def init_db():
    """Initialize database"""
    # Удаляем все существующие таблицы
    Base.metadata.drop_all(bind=engine)
    # Создаем таблицы заново
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db() 