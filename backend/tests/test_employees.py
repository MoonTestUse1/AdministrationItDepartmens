"""Employee tests"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

def test_create_employee(client: TestClient, admin_token: str):
    """Test employee creation"""
    response = client.post(
        "/api/employees",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "first_name": "New",
            "last_name": "Employee",
            "department": "IT",
            "office": "103",
            "password": "newpass123",
            "is_admin": False
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "New"
    assert data["last_name"] == "Employee"
    assert data["department"] == "IT"
    assert data["office"] == "103"
    assert data["is_admin"] == False

def test_create_employee_unauthorized(client: TestClient):
    """Test employee creation without authorization"""
    response = client.post(
        "/api/employees",
        json={
            "first_name": "New",
            "last_name": "Employee",
            "department": "IT",
            "office": "103",
            "password": "newpass123",
            "is_admin": False
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_create_employee_not_admin(client: TestClient, employee_token: str):
    """Test employee creation by non-admin user"""
    response = client.post(
        "/api/employees",
        headers={"Authorization": f"Bearer {employee_token}"},
        json={
            "first_name": "New",
            "last_name": "Employee",
            "department": "IT",
            "office": "103",
            "password": "newpass123",
            "is_admin": False
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Not enough permissions"

def test_get_employees(client: TestClient, admin_token: str):
    """Test getting all employees"""
    response = client.get(
        "/api/employees",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_employees_unauthorized(client: TestClient):
    """Test getting employees without authorization"""
    response = client.get("/api/employees")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_get_employees_not_admin(client: TestClient, employee_token: str):
    """Test getting employees by non-admin user"""
    response = client.get(
        "/api/employees",
        headers={"Authorization": f"Bearer {employee_token}"}
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Not enough permissions"

def test_get_me(client: TestClient, employee_token: str, test_employee: dict):
    """Test getting current employee"""
    response = client.get(
        "/api/employees/me",
        headers={"Authorization": f"Bearer {employee_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == test_employee.first_name
    assert data["last_name"] == test_employee.last_name
    assert data["department"] == test_employee.department
    assert data["office"] == test_employee.office

def test_get_me_unauthorized(client: TestClient):
    """Test getting current employee without authorization"""
    response = client.get("/api/employees/me")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_update_me(client: TestClient, employee_token: str):
    """Test updating current employee"""
    response = client.put(
        "/api/employees/me",
        headers={"Authorization": f"Bearer {employee_token}"},
        json={
            "department": "HR",
            "office": "104"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["department"] == "HR"
    assert data["office"] == "104"

def test_update_me_unauthorized(client: TestClient):
    """Test updating current employee without authorization"""
    response = client.put(
        "/api/employees/me",
        json={
            "department": "HR",
            "office": "104"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated" 