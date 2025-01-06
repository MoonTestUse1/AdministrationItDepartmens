"""Test configuration."""
import pytest
from typing import Generator
from fastapi.testclient import TestClient
from unittest.mock import patch

from .test_config import engine, TestingSessionLocal
from app.database import get_db
from app.models.base import Base
from app.models.employee import Employee
from app.utils.auth import get_password_hash

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
    from app.main import app

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
        first_name="Test",
        last_name="User",
        department="IT",
        office="101",
        hashed_password=get_password_hash("testpassword")
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee

@pytest.fixture(scope="function")
def test_admin(db: TestingSessionLocal) -> Employee:
    """Фикстура для создания тестового администратора."""
    admin = Employee(
        first_name="Admin",
        last_name="User",
        department="Administration",
        office="100",
        hashed_password=get_password_hash("adminpassword")
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