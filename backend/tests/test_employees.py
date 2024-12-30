"""Employee management endpoint tests"""
import pytest
from app.models.employee import EmployeeCreate

def test_create_employee(client, test_employee):
    """Test employee creation"""
    response = client.post(
        "/api/employees",
        json={
            "first_name": test_employee["first_name"],
            "last_name": test_employee["last_name"],
            "department": test_employee["department"],
            "office": test_employee["office"],
            "password": test_employee["password"]
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["firstName"] == test_employee["first_name"]
    assert data["lastName"] == test_employee["last_name"]
    assert "password" not in data

def test_create_employee_duplicate(client, test_employee):
    """Test creating duplicate employee"""
    # Create first employee
    client.post(
        "/api/employees",
        json={
            "first_name": test_employee["first_name"],
            "last_name": test_employee["last_name"],
            "department": test_employee["department"],
            "office": test_employee["office"],
            "password": test_employee["password"]
        }
    )
    
    # Try to create duplicate
    response = client.post(
        "/api/employees",
        json={
            "first_name": test_employee["first_name"],
            "last_name": test_employee["last_name"],
            "department": test_employee["department"],
            "office": test_employee["office"],
            "password": test_employee["password"]
        }
    )
    
    assert response.status_code == 400
    assert "уже существует" in response.json()["detail"]

def test_create_employee_invalid_data(client):
    """Test creating employee with invalid data"""
    invalid_employee = {
        "first_name": "",  # Empty name
        "last_name": "Test",
        "department": "invalid",  # Invalid department
        "office": "101",
        "password": "test"
    }
    
    response = client.post(
        "/api/employees",
        json=invalid_employee
    )
    
    assert response.status_code == 422