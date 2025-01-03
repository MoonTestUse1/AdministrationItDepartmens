import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import Mock, patch
from ..database import Base, get_db
from ..main import app
from ..utils.jwt import create_and_save_token
from ..crud import employees
from ..utils.auth import get_password_hash

# Используем SQLite для тестов
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Мок для Redis
class MockRedis:
    def __init__(self):
        self.data = {}
    
    def setex(self, name, time, value):
        self.data[name] = value
        return True
    
    def get(self, name):
        return self.data.get(name)

@pytest.fixture(autouse=True)
def mock_redis():
    with patch("app.utils.jwt.redis", MockRedis()):
        yield

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
    hashed_password = get_password_hash("testpass123")
    employee_data = {
        "first_name": "Test",
        "last_name": "User",
        "department": "IT",
        "office": "101"
    }
    employee = employees.create_employee(test_db, employee_data, hashed_password=hashed_password)
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