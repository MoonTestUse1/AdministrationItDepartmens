import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.crud import employees
from app.utils.auth import verify_password, get_password_hash
from app.schemas.employee import EmployeeCreate

client = TestClient(app)

def test_login_success(test_db: Session):
    # Создаем тестового сотрудника
    hashed_password = get_password_hash("testpass123")
    employee_data = EmployeeCreate(
        first_name="Test",
        last_name="User",
        department="IT",
        office="101",
        password="testpass123"
    )
    employee = employees.create_employee(test_db, employee_data, hashed_password)
    
    response = client.post(
        "/api/auth/login",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": "User",
            "password": "testpass123"
        }
    )
    
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_wrong_password(test_db: Session):
    # Создаем тестового сотрудника
    hashed_password = get_password_hash("testpass123")
    employee_data = EmployeeCreate(
        first_name="Test",
        last_name="User",
        department="IT",
        office="101",
        password="testpass123"
    )
    employees.create_employee(test_db, employee_data, hashed_password)
    
    response = client.post(
        "/api/auth/login",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": "User",
            "password": "wrongpass"
        }
    )
    
    assert response.status_code == 401
    assert "detail" in response.json()

def test_login_nonexistent_user(test_db: Session):
    response = client.post(
        "/api/auth/login",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": "NonExistent",
            "password": "testpass123"
        }
    )
    
    assert response.status_code == 401
    assert "detail" in response.json()

def test_admin_login_success():
    response = client.post(
        "/api/auth/admin/login",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": "admin",
            "password": "admin123"
        }
    )
    
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_admin_login_wrong_password():
    response = client.post(
        "/api/auth/admin/login",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": "admin",
            "password": "wrongpass"
        }
    )
    
    assert response.status_code == 401
    assert "detail" in response.json() 