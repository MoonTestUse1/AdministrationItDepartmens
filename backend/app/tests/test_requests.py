import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from ..main import app
from ..models.request import RequestStatus, RequestPriority
from ..crud import requests, employees
from ..utils.auth import get_password_hash

client = TestClient(app)

def test_create_request(test_db: Session, test_token: str):
    request_data = {
        "department": "IT",
        "request_type": "hardware",
        "priority": RequestPriority.LOW.value,
        "description": "Test Description"
    }
    
    response = client.post(
        "/api/requests/",
        json=request_data,
        headers={"Authorization": f"Bearer {test_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["department"] == request_data["department"]
    assert data["description"] == request_data["description"]
    assert data["priority"] == RequestPriority.LOW.value
    assert data["status"] == RequestStatus.NEW.value

def test_create_request_unauthorized():
    request_data = {
        "department": "IT",
        "request_type": "hardware",
        "priority": RequestPriority.LOW.value,
        "description": "Test Description"
    }
    
    response = client.post(
        "/api/requests/",
        json=request_data
    )
    
    assert response.status_code == 401

def test_get_employee_requests(test_db: Session, test_token: str, test_employee_id: int):
    # Создаем несколько тестовых заявок
    for i in range(3):
        requests.create_request(
            test_db,
            {
                "department": "IT",
                "request_type": f"hardware_{i}",
                "priority": RequestPriority.LOW.value,
                "description": f"Test Description {i}"
            },
            test_employee_id
        )
    
    response = client.get(
        "/api/requests/",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert all(req["employee_id"] == test_employee_id for req in data)

def test_update_request_status(test_db: Session, admin_token: str):
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
    
    # Создаем тестовую заявку
    request = requests.create_request(
        test_db,
        {
            "department": "IT",
            "request_type": "hardware",
            "priority": RequestPriority.LOW.value,
            "description": "Test Description"
        },
        employee.id
    )
    
    response = client.put(
        f"/api/requests/{request.id}",
        json={"status": RequestStatus.IN_PROGRESS.value},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    assert response.json()["status"] == RequestStatus.IN_PROGRESS.value

def test_get_request_statistics(test_db: Session, admin_token: str):
    response = client.get(
        "/api/requests/statistics",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "total_requests" in data
    assert "by_status" in data
    assert RequestStatus.NEW.value in data["by_status"]
    assert RequestStatus.IN_PROGRESS.value in data["by_status"]
    assert RequestStatus.COMPLETED.value in data["by_status"]
    assert RequestStatus.REJECTED.value in data["by_status"] 