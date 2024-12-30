"""Test configuration and fixtures"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import logging

from app.database import Base, get_db
from app.main import app

# Configure logging for tests
logging.basicConfig(level=logging.INFO)

# Create test database
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Override database dependency"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def test_db():
    """Create test database"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(test_db):
    """Create test client"""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def test_employee():
    """Test employee data"""
    return {
        "first_name": "Test",
        "last_name": "User",
        "department": "general",
        "office": "101",
        "password": "testpass123"
    }

@pytest.fixture
def test_request():
    """Test request data"""
    return {
        "employee_id": 1,
        "department": "general",
        "request_type": "hardware",
        "priority": "medium",
        "description": "Test request"
    }