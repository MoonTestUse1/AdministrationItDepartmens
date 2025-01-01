import pytest
from app.models.employee import Employee
from app.utils.auth import get_password_hash

def test_admin_login(client):
    """Test admin login endpoint"""
    response = client.post("/api/auth/admin", json={
        "username": "admin",
        "password": "admin123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_admin_login_invalid_credentials(client):
    """Test admin login with invalid credentials"""
    response = client.post("/api/auth/admin", json={
        "username": "wrong",
        "password": "wrong"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_employee_login(client, db_session):
    """Test employee login endpoint"""
    # Create test employee
    hashed_password = get_password_hash("test123")
    employee = Employee(
        first_name="Test",
        last_name="User",
        department="IT",
        office="A101",
        password=hashed_password
    )
    db_session.add(employee)
    db_session.commit()

    # Try to login
    response = client.post("/api/auth/login", json={
        "last_name": "User",
        "password": "test123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Test"
    assert data["last_name"] == "User"
    assert data["department"] == "IT"
    assert data["office"] == "A101"
    assert "access_token" in data

def test_employee_login_invalid_credentials(client, db_session):
    """Test employee login with invalid credentials"""
    # Create test employee
    hashed_password = get_password_hash("test123")
    employee = Employee(
        first_name="Test",
        last_name="User",
        department="IT",
        office="A101",
        password=hashed_password
    )
    db_session.add(employee)
    db_session.commit()

    # Try to login with wrong password
    response = client.post("/api/auth/login", json={
        "last_name": "User",
        "password": "wrong"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Неверный пароль" 