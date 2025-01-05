"""Test configuration."""
import pytest
from typing import Generator, Dict
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from app.core.config import settings
from app.models.user import User
from app.core.auth import get_password_hash

# Создаем тестовую базу данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем фиктивный Redis для тестов
class FakeRedis:
    """Fake Redis for testing."""
    def __init__(self):
        self.data = {}

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value, ex=None):
        self.data[key] = value

    def delete(self, key):
        if key in self.data:
            del self.data[key]

@pytest.fixture(scope="session")
def redis():
    """Redis fixture."""
    return FakeRedis()

def override_get_db():
    """Override get_db for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Setup database for testing."""
    # Создаем все таблицы
    Base.metadata.create_all(bind=engine)
    yield
    # Удаляем все таблицы после тестов
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db() -> Generator:
    """Database fixture."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db) -> Generator:
    """Test client fixture."""
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function")
def test_user(db) -> Dict[str, str]:
    """Test user fixture."""
    user_data = {
        "email": "test@example.com",
        "password": "test123",
        "full_name": "Test User",
        "is_admin": False
    }
    
    user = User(
        email=user_data["email"],
        hashed_password=get_password_hash(user_data["password"]),
        full_name=user_data["full_name"],
        is_admin=user_data["is_admin"]
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user_data

@pytest.fixture(scope="function")
def test_admin(db) -> Dict[str, str]:
    """Test admin fixture."""
    admin_data = {
        "email": "admin@example.com",
        "password": "admin123",
        "full_name": "Admin User",
        "is_admin": True
    }
    
    admin = User(
        email=admin_data["email"],
        hashed_password=get_password_hash(admin_data["password"]),
        full_name=admin_data["full_name"],
        is_admin=admin_data["is_admin"]
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    
    return admin_data 