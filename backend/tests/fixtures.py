"""Test fixtures"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.crud import employees
from app.schemas.employee import EmployeeCreate
from app.utils.auth import get_password_hash
from app.models.employee import Employee

@pytest.fixture(scope="function")
def test_employee(db_session: Session) -> Employee:
    """Create test employee"""
    # Удаляем существующего сотрудника, если есть
    db_session.query(Employee).filter(
        Employee.first_name == "Test",
        Employee.last_name == "User"
    ).delete()
    db_session.commit()

    employee = EmployeeCreate(
        first_name="Test",
        last_name="User",
        department="IT",
        office="101",
        password="testpass123",
        is_admin=False
    )
    hashed_password = get_password_hash(employee.password)
    db_employee = employees.create_employee(db_session, employee, hashed_password)
    return db_employee

@pytest.fixture(scope="function")
def test_admin(db_session: Session) -> Employee:
    """Create test admin"""
    # Удаляем существующего админа, если есть
    db_session.query(Employee).filter(
        Employee.first_name == "Admin",
        Employee.last_name == "User"
    ).delete()
    db_session.commit()

    admin = EmployeeCreate(
        first_name="Admin",
        last_name="User",
        department="IT",
        office="102",
        password="adminpass123",
        is_admin=True
    )
    hashed_password = get_password_hash(admin.password)
    db_admin = employees.create_employee(db_session, admin, hashed_password)
    return db_admin

@pytest.fixture(scope="function")
def employee_token(client: TestClient, test_employee: Employee) -> str:
    """Get employee token"""
    response = client.post(
        "/api/auth/login",
        data={
            "username": f"{test_employee.first_name} {test_employee.last_name}",
            "password": "testpass123"
        }
    )
    return response.json()["access_token"]

@pytest.fixture(scope="function")
def admin_token(client: TestClient, test_admin: Employee) -> str:
    """Get admin token"""
    response = client.post(
        "/api/auth/admin/login",
        data={
            "username": f"{test_admin.first_name} {test_admin.last_name}",
            "password": "adminpass123"
        }
    )
    return response.json()["access_token"] 