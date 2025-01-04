"""Database session configuration"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .db.base import Base
from .config import settings

# Создаем URL для подключения к базе данных
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Создаем движок SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()