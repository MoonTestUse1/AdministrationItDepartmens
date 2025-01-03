import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from ..database import Base, get_db
from ..main import app
from ..utils.jwt import create_and_save_token
from ..crud import employees

# Получаем URL базы данных из переменной окружения или используем значение по умолчанию
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/support_test"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def test_db():
    # Создаем таблицы
    Base.metadata.create_all(bind=engine)
    
    # Создаем сессию
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Очищаем таблицы после каждого теста
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def test_employee(test_db):
    employee_data = {
        "first_name": "Test",
        "last_name": "User",
        "department": "IT",
        "office": "101",
        "password": "testpass123"
    }
    employee = employees.create_employee(test_db, employee_data)
    return employee

@pytest.fixture(scope="function")
def test_token(test_db, test_employee):
    return create_and_save_token(test_employee.id, test_db)

@pytest.fixture(scope="function")
def admin_token(test_db):
    return create_and_save_token(-1, test_db)  # -1 для админа

@pytest.fixture(scope="function")
def test_employee_id(test_employee):
    return test_employee.id

# Переопределяем зависимость для получения БД
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db 