"""Test configuration."""
import os
import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from unittest.mock import Mock, patch

from app.database import Base, get_db
from app.main import app
from app.models.employee import Employee
from app.utils.auth import get_password_hash
from app.utils.jwt import create_access_token
from app.core.config import settings

# Создаем тестовую базу данных в памяти
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class MockRedis:
    """Мок для Redis."""
    def __init__(self):
        self.data = {}

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value, ex=None):
        self.data[key] = value
        return True

    def delete(self, key):
        if key in self.data:
            del self.data[key]
        return True

    def exists(self, key):
        return key in self.data

@pytest.fixture(scope="function")
def redis_mock():
    """Фикстура для мока Redis."""
    with patch("app.utils.jwt.redis") as mock:
        redis_instance = MockRedis()
        mock.get.side_effect = redis_instance.get
        mock.set.side_effect = redis_instance.set
        mock.delete.side_effect = redis_instance.delete
        mock.exists.side_effect = redis_instance.exists
        yield mock

@pytest.fixture(scope="function")
def db() -> Generator:
    """Фикстура для создания тестовой базы данных."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db: TestingSessionLocal, redis_mock) -> Generator:
    """Фикстура для создания тестового клиента."""
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture(scope="function")
def test_employee(db: TestingSessionLocal) -> Employee:
    """Фикстура для создания тестового сотрудника."""
    employee = Employee(
        email="test@example.com",
        full_name="Test Employee",
        hashed_password=get_password_hash("testpassword"),
        is_active=True,
        is_admin=False,
        department="IT"
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee

@pytest.fixture(scope="function")
def test_admin(db: TestingSessionLocal) -> Employee:
    """Фикстура для создания тестового администратора."""
    admin = Employee(
        email="admin@example.com",
        full_name="Test Admin",
        hashed_password=get_password_hash("adminpassword"),
        is_active=True,
        is_admin=True,
        department="Administration"
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin

@pytest.fixture(scope="function")
def employee_token(test_employee: Employee, db: TestingSessionLocal) -> str:
    """Фикстура для создания токена тестового сотрудника."""
    from app.utils.jwt import create_access_token
    token = create_access_token({"sub": str(test_employee.id)})
    # Сохраняем токен в Redis мок
    from app.utils.jwt import redis
    redis.set(f"token:{token}", "valid")
    return token

@pytest.fixture(scope="function")
def admin_token(test_admin: Employee, db: TestingSessionLocal) -> str:
    """Фикстура для создания токена администратора."""
    from app.utils.jwt import create_access_token
    token = create_access_token({"sub": str(test_admin.id)})
    # Сохраняем токен в Redis мок
    from app.utils.jwt import redis
    redis.set(f"token:{token}", "valid")
    return token 