"""Test configuration"""
import os
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from typing import Generator, Any

# Устанавливаем переменную окружения для тестов
os.environ["TESTING"] = "True"

from app.database import Base
from app.main import app
from app.core.test_config import test_settings
from app.dependencies import get_db
from .fixtures import *  # импортируем все фикстуры

# Создаем тестовый движок базы данных
engine = create_engine(test_settings.DATABASE_URL)

# Создаем тестовую фабрику сессий
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db() -> Generator[None, Any, None]:
    """Setup test database"""
    # Пробуем создать базу данных test_app
    default_engine = create_engine("postgresql://postgres:postgres@localhost:5432/postgres")
    with default_engine.connect() as conn:
        conn.execute(text("COMMIT"))  # Завершаем текущую транзакцию
        try:
            conn.execute(text("DROP DATABASE IF EXISTS test_app"))
            conn.execute(text("CREATE DATABASE test_app"))
        except Exception as e:
            print(f"Error creating database: {e}")
    
    # Создаем все таблицы
    Base.metadata.create_all(bind=engine)
    yield
    # Удаляем все таблицы
    Base.metadata.drop_all(bind=engine)
    
    # Закрываем соединение с тестовой базой
    engine.dispose()

@pytest.fixture
def db_session() -> Generator[Any, Any, None]:
    """Get database session"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture
def client(db_session: Any) -> Generator[TestClient, Any, None]:
    """Get test client"""
    def override_get_db() -> Generator[Any, Any, None]:
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear() 