"""Database session configuration"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .db.base_class import Base
from .config import settings
import logging

# Настраиваем логирование
logger = logging.getLogger(__name__)

# Создаем URL для подключения к базе данных
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
logger.info(f"Database URL: {SQLALCHEMY_DATABASE_URL}")

# Создаем движок SQLAlchemy с логированием SQL-запросов
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,  # Включаем логирование SQL-запросов
    pool_pre_ping=True,  # Проверяем соединение перед использованием
    pool_size=5,  # Размер пула соединений
    max_overflow=10  # Максимальное количество дополнительных соединений
)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция для получения сессии базы данных
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()