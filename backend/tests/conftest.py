"""Test configuration"""
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.test_config import test_settings
from app.db.base_class import Base
from app.models.employee import Employee
from app.models.request import Request
from app.models.token import Token
from app.main import app
from app.dependencies import get_db
from app.utils.security import get_password_hash
from app.utils.jwt import create_and_save_token

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
    database_url = test_settings.get_database_url()
    engine = create_engine(
        database_url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10
    )
    # Создаем все таблицы перед тестами
    Base.metadata.drop_all(bind=engine)
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

@pytest.fixture
def employee_token(test_employee, db_session):
    """Create employee token"""
    return create_and_save_token(test_employee.id, db_session)

@pytest.fixture
def admin_token(test_admin, db_session):
    """Create admin token"""
    return create_and_save_token(test_admin.id, db_session)

@pytest.fixture
def employee_headers(employee_token):
    """Get employee headers"""
    return {"Authorization": f"Bearer {employee_token}"}

@pytest.fixture
def admin_headers(admin_token):
    """Get admin headers"""
    return {"Authorization": f"Bearer {admin_token}"} 