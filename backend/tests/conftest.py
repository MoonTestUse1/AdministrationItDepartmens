"""Test configuration"""
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.db.base import Base
from app.main import app
from app.deps import get_db
from app.models.employee import Employee
from app.utils.security import get_password_hash

# Mock Telegram notifications
@pytest.fixture(autouse=True)
def mock_telegram_bot(mocker):
    """Mock Telegram Bot"""
    mock_bot = mocker.patch('app.utils.telegram.Bot')
    return mock_bot

@pytest.fixture(autouse=True)
def mock_telegram_notify(mocker):
    """Mock Telegram notifications"""
    mocker.patch('app.utils.telegram.notify_new_request', return_value=None)

# Database fixtures
@pytest.fixture(scope="session")
def engine():
    """Create test database engine"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    return engine

@pytest.fixture(scope="function")
def db_session(engine):
    """Create test database session"""
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

@pytest.fixture
def client(db_session):
    """Create test client"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture
def test_employee(db_session):
    """Create test employee"""
    employee = Employee(
        first_name="Test",
        last_name="User",
        department="IT",
        office="Main",
        hashed_password=get_password_hash("testpass123"),
        is_active=True,
        is_admin=False
    )
    db_session.add(employee)
    db_session.commit()
    db_session.refresh(employee)
    return employee

@pytest.fixture
def test_admin(db_session):
    """Create test admin"""
    admin = Employee(
        first_name="Admin",
        last_name="User",
        department="IT",
        office="Main",
        hashed_password=get_password_hash("adminpass123"),
        is_active=True,
        is_admin=True
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin 