"""Test configuration"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Используем SQLite в памяти для тестов
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Создаем тестовый движок
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

# Создаем фабрику сессий
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 