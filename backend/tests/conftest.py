import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import MagicMock
from app.db.base import Base
from app.database import get_db
from app.main import app
from app.utils.jwt import create_and_save_token, redis
from app.crud import employees
from app.utils.auth import get_password_hash
from app.models.token import Token
from app.models.employee import Employee
from app.models.request import Request
from app.schemas.employee import EmployeeCreate

# Используем SQLite для тестов
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем мок для Redis
class RedisMock:
    def __init__(self):
        self.data = {}

    def setex(self, name, time, value):
        self.data[name] = value
        return True

    def get(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        return True

@pytest.fixture(autouse=True)
def mock_redis(monkeypatch):
    redis_mock = RedisMock()
    monkeypatch.setattr("app.utils.jwt.redis", redis_mock)
    return redis_mock

@pytest.fixture(scope="function")
def test_db():
    # Удаляем все таблицы
    Base.metadata.drop_all(bind=engine)
    # Создаем все таблицы заново
    Base.metadata.create_all(bind=engine)
    
    # Создаем сессию
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def test_employee(test_db):
    hashed_password = get_password_hash("testpass123")
    employee_data = EmployeeCreate(
        first_name="Test",
        last_name="User",
        department="IT",
        office="101",
        password="testpass123"
    )
    employee = employees.create_employee(test_db, employee_data, hashed_password)
    return employee

@pytest.fixture(scope="function")
def test_token(test_db, test_employee):
    token = create_and_save_token(test_employee.id, test_db)
    return token

@pytest.fixture(scope="function")
def test_auth_header(test_token):
    return {"Authorization": f"Bearer {test_token}"}

@pytest.fixture(scope="function")
def admin_token(test_db):
    token = create_and_save_token(-1, test_db)  # -1 для админа
    return token

@pytest.fixture(scope="function")
def admin_auth_header(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}

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