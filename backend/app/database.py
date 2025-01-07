"""Database module"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from .core.config import settings

# Создаем базовый класс для моделей
Base = declarative_base()

# Создаем движок базы данных
engine = create_engine(
    settings.get_database_url(),
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize database"""
    # Импортируем модели здесь, чтобы избежать циклических зависимостей
    from .db.base import Base  # noqa: F811
    Base.metadata.create_all(bind=engine)