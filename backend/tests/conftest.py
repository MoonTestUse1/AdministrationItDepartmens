"""Test fixtures"""
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import fakeredis.aioredis
from typing import Generator

# Устанавливаем флаг тестирования
os.environ["TESTING"] = "True"

from app.main import app
from app.database import Base, get_db
from app.models.employee import Employee
from app.utils.auth import get_password_hash

# Создаем тестовую базу данных в памяти
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем тестовую базу данных
Base.metadata.create_all(bind=engine)

@pytest.fixture
def db() -> Generator:
    """Фикстура для получения тестовой сессии БД."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db) -> TestClient:
    """Фикстура для получения тестового клиента."""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def test_employee(db) -> Employee:
    """Фикстура для создания тестового сотрудника."""
    employee = Employee(
        first_name="Test",
        last_name="Employee",
        department="Test Department",
        office="Test Office",
        hashed_password=get_password_hash("testpassword"),
        is_admin=False
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee

@pytest.fixture
def test_admin(db) -> Employee:
    """Фикстура для создания тестового администратора."""
    admin = Employee(
        first_name="Admin",
        last_name="User",
        department="Admin Department",
        office="Admin Office",
        hashed_password=get_password_hash("adminpassword"),
        is_admin=True
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin

@pytest.fixture
def employee_token(client: TestClient, test_employee: Employee) -> str:
    """Фикстура для получения токена сотрудника."""
    response = client.post(
        "/api/auth/login",
        data={"username": test_employee.last_name, "password": "testpassword"}
    )
    return response.json()["access_token"]

@pytest.fixture
def admin_token(client: TestClient, test_admin: Employee) -> str:
    """Фикстура для получения токена администратора."""
    response = client.post(
        "/api/auth/admin/login",
        data={"username": test_admin.last_name, "password": "adminpassword"}
    )
    return response.json()["access_token"]

@pytest.fixture
def redis_mock():
    """Фикстура для мока Redis."""
    return fakeredis.aioredis.FakeRedis() 