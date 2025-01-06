"""Database configuration"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .core.config import settings

# Для создания таблиц импортируем модели
from .models.employee import Employee  # noqa
from .models.request import Request  # noqa
from .models.token import Token  # noqa

def get_database_url():
    """Получение URL базы данных в зависимости от окружения."""
    try:
        from .core.test_config import test_settings
        return test_settings.DATABASE_URL
    except ImportError:
        return settings.DATABASE_URL

# Используем правильный URL для базы данных
SQLALCHEMY_DATABASE_URL = get_database_url()

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