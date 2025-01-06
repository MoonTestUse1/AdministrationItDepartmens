"""Authentication tests"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

def test_login_success(client: TestClient, test_employee: dict):
    """Test successful login"""
    response = client.post(
        "/api/auth/login",
        data={
            "username": f"{test_employee.first_name} {test_employee.last_name}",
            "password": "testpass123"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_wrong_password(client: TestClient, test_employee: dict):
    """Test login with wrong password"""
    response = client.post(
        "/api/auth/login",
        data={
            "username": f"{test_employee.first_name} {test_employee.last_name}",
            "password": "wrongpass"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

def test_login_wrong_username(client: TestClient):
    """Test login with wrong username"""
    response = client.post(
        "/api/auth/login",
        data={
            "username": "Wrong User",
            "password": "testpass123"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

def test_login_invalid_username_format(client: TestClient):
    """Test login with invalid username format"""
    response = client.post(
        "/api/auth/login",
        data={
            "username": "InvalidFormat",
            "password": "testpass123"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Username should be in format: 'First Last'"

def test_admin_login_success(client: TestClient, test_admin: dict):
    """Test successful admin login"""
    response = client.post(
        "/api/auth/admin/login",
        data={
            "username": f"{test_admin.first_name} {test_admin.last_name}",
            "password": "adminpass123"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_admin_login_not_admin(client: TestClient, test_employee: dict):
    """Test admin login with non-admin user"""
    response = client.post(
        "/api/auth/admin/login",
        data={
            "username": f"{test_employee.first_name} {test_employee.last_name}",
            "password": "testpass123"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

def test_protected_route_with_invalid_token(client: TestClient):
    """Test accessing protected route with invalid token"""
    response = client.get(
        "/api/employees/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid authentication credentials" 