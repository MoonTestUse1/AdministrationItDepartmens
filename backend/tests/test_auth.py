"""Authentication endpoint tests"""
import pytest
from app.crud import employees
from app.models.employee import EmployeeCreate

def test_login_success(client, test_db, test_employee):
    """Test successful login"""
    # Create test employee
    employee_data = EmployeeCreate(**test_employee)
    employees.create_employee(test_db, employee_data)
    
    # Attempt login
    response = client.post(
        "/api/auth/login",
        json={
            "lastName": test_employee["last_name"],
            "password": test_employee["password"]
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["lastName"] == test_employee["last_name"]
    assert "password" not in data

def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    response = client.post(
        "/api/auth/login",
        json={
            "lastName": "NonExistent",
            "password": "wrongpass"
        }
    )
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Неверные учетные данные"

def test_login_missing_fields(client):
    """Test login with missing fields"""
    response = client.post(
        "/api/auth/login",
        json={"lastName": "Test"}
    )
    
    assert response.status_code == 400
    assert "Необходимо указать" in response.json()["detail"]