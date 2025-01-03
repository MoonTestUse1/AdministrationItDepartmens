import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.crud import employees
from app.utils.auth import get_password_hash
from app.schemas.employee import EmployeeCreate

client = TestClient(app)

def test_create_employee(test_db: Session, admin_auth_header):
    """Test creating a new employee"""
    employee_data = {
        "first_name": "John",
        "last_name": "Doe",
        "department": "IT",
        "office": "B205",
        "password": "test123"
    }
    
    response = client.post(
        "/api/employees/",
        json=employee_data,
        headers=admin_auth_header
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == employee_data["first_name"]
    assert data["last_name"] == employee_data["last_name"]
    assert data["department"] == employee_data["department"]
    assert data["office"] == employee_data["office"]
    assert "password" not in data

def test_get_employees(test_db: Session, test_employee, admin_auth_header):
    """Test getting list of employees"""
    response = client.get("/api/employees/", headers=admin_auth_header)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["first_name"] == test_employee.first_name
    assert data[0]["last_name"] == test_employee.last_name
    assert data[0]["department"] == test_employee.department
    assert data[0]["office"] == test_employee.office
    assert "password" not in data[0]

def test_create_employee_unauthorized(test_db: Session):
    """Test creating employee without authorization"""
    employee_data = {
        "first_name": "John",
        "last_name": "Doe",
        "department": "IT",
        "office": "B205",
        "password": "test123"
    }
    response = client.post("/api/employees/", json=employee_data)
    assert response.status_code == 401  # Unauthorized

def test_get_employees_unauthorized(test_db: Session):
    """Test getting employees list without authorization"""
    response = client.get("/api/employees/")
    assert response.status_code == 401  # Unauthorized

def test_get_employee_by_id(test_db: Session, test_employee, admin_auth_header):
    """Test getting employee by ID"""
    response = client.get(
        f"/api/employees/{test_employee.id}",
        headers=admin_auth_header
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == test_employee.first_name
    assert data["last_name"] == test_employee.last_name
    assert data["department"] == test_employee.department
    assert data["office"] == test_employee.office
    assert "password" not in data

def test_update_employee(test_db: Session, test_employee, admin_auth_header):
    """Test updating employee data"""
    update_data = {
        "first_name": "Updated",
        "last_name": "Name",
        "department": "HR",
        "office": "B202"
    }
    
    response = client.put(
        f"/api/employees/{test_employee.id}",
        json=update_data,
        headers=admin_auth_header
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == update_data["first_name"]
    assert data["last_name"] == update_data["last_name"]
    assert data["department"] == update_data["department"]
    assert data["office"] == update_data["office"]
    assert "password" not in data

def test_delete_employee(test_db: Session, test_employee, admin_auth_header):
    """Test deleting employee"""
    response = client.delete(
        f"/api/employees/{test_employee.id}",
        headers=admin_auth_header
    )
    
    assert response.status_code == 200
    
    # Verify employee is deleted
    get_response = client.get(
        f"/api/employees/{test_employee.id}",
        headers=admin_auth_header
    )
    assert get_response.status_code == 404 