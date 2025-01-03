import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from ..main import app
from ..crud import employees
from ..utils.auth import verify_password, get_password_hash

client = TestClient(app)

def test_create_employee(test_db: Session, admin_token: str):
    employee_data = {
        "first_name": "John",
        "last_name": "Doe",
        "department": "IT",
        "office": "101",
        "password": "testpass123"
    }
    
    response = client.post(
        "/api/employees/",
        json=employee_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == employee_data["first_name"]
    assert data["last_name"] == employee_data["last_name"]
    assert data["department"] == employee_data["department"]
    assert data["office"] == employee_data["office"]
    assert "id" in data

def test_create_employee_unauthorized():
    employee_data = {
        "first_name": "John",
        "last_name": "Doe",
        "department": "IT",
        "office": "101",
        "password": "testpass123"
    }
    
    response = client.post(
        "/api/employees/",
        json=employee_data
    )
    
    assert response.status_code == 401

def test_get_employees(test_db: Session, admin_token: str):
    # Создаем несколько тестовых сотрудников
    for i in range(3):
        hashed_password = get_password_hash("testpass123")
        employees.create_employee(
            test_db,
            {
                "first_name": f"Test{i}",
                "last_name": f"User{i}",
                "department": "IT",
                "office": f"10{i}"
            },
            hashed_password=hashed_password
        )
    
    response = client.get(
        "/api/employees/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3

def test_get_employee_by_id(test_db: Session, admin_token: str):
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
    
    response = client.get(
        f"/api/employees/{employee.id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == employee.id
    assert data["first_name"] == employee.first_name
    assert data["last_name"] == employee.last_name

def test_update_employee(test_db: Session, admin_token: str):
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
    
    update_data = {
        "department": "HR",
        "office": "202"
    }
    
    response = client.put(
        f"/api/employees/{employee.id}",
        json=update_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["department"] == update_data["department"]
    assert data["office"] == update_data["office"]

def test_delete_employee(test_db: Session, admin_token: str):
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
    
    response = client.delete(
        f"/api/employees/{employee.id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    
    # Проверяем, что сотрудник удален
    get_response = client.get(
        f"/api/employees/{employee.id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert get_response.status_code == 404 