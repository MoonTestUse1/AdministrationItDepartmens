"""Test configuration"""
import os
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from fastapi.testclient import TestClient
from typing import Generator, Any

# Устанавливаем переменную окружения для тестов
os.environ["TESTING"] = "1"

from app.database import Base
from app.main import app
from app.core.test_config import test_settings
from app.dependencies import get_db
from .test_fixtures import *  # импортируем все фикстуры

# Создаем тестовый движок базы данных
DATABASE_URL = os.getenv("DATABASE_URL", test_settings.get_database_url())
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_pre_ping=True
)

# Создаем тестовую фабрику сессий
TestingSessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db() -> Generator[None, Any, None]:
    """Setup test database"""
    # Создаем все таблицы
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    # Удаляем все таблицы и закрываем соединения
    TestingSessionLocal.remove()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()

@pytest.fixture(scope="function")
def db_session() -> Generator[Any, Any, None]:
    """Get database session"""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
        TestingSessionLocal.remove()

@pytest.fixture(scope="function")
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