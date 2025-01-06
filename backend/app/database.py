"""Database module"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .core.config import settings

# Определяем, используем ли тестовую базу данных
TESTING = os.getenv("TESTING", "False") == "True"
DATABASE_URL = "sqlite:///:memory:" if TESTING else settings.DATABASE_URL

# Создаем базовый класс для моделей
Base = declarative_base()

# Создаем движок базы данных
connect_args = {"check_same_thread": False} if TESTING else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()