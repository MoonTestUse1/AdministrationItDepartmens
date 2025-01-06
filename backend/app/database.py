"""Database configuration"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from .core.config import settings

# Создаем движок базы данных
engine = create_engine(settings.get_database_url())

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем базовый класс для моделей
Base = declarative_base()

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()