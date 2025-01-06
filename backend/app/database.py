"""Database configuration"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .core.config import settings

# Для создания таблиц импортируем модели
from .models.employee import Employee  # noqa
from .models.request import Request  # noqa
from .models.token import Token  # noqa

# Используем разные URL для тестов и продакшена
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Создаем движок с нужными параметрами
connect_args = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=connect_args
)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Получение сессии базы данных."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()