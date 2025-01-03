import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from ..main import app
from ..crud import employees
from ..utils.auth import verify_password, get_password_hash

client = TestClient(app)

def test_login_success(test_db: Session):
    # Создаем тестового сотрудника
    hashed_password = get_password_hash("testpass123")
    employee = employees.create_employee(
        test_db,
        {
            "first_name": "Test",
            "last_name": "User",
            "department": "IT",
            "office": "101"
        },
        hashed_password=hashed_password
    )
    
    response = client.post(
        "/api/auth/login",
        data={
            "username": "User",
            "password": "testpass123"
        }
    )
    
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_wrong_password(test_db: Session):
    hashed_password = get_password_hash("testpass123")
    employee = employees.create_employee(
        test_db,
        {
            "first_name": "Test",
            "last_name": "WrongPass",
            "department": "IT",
            "office": "101"
        },
        hashed_password=hashed_password
    )
    
    response = client.post(
        "/api/auth/login",
        data={"username": "WrongPass",
            "password": "wrongpass"}
    )
    assert response.status_code == 401
    assert "detail" in response.json()

def test_login_nonexistent_user(test_db: Session):
    response = client.post(
        "/api/auth/login",
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
        data={
            "username": "admin",
            "password": "wrongpass"
        }
    )
    
    assert response.status_code == 401
    assert "detail" in response.json() 