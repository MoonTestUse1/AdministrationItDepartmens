import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from ..main import app
from ..crud import requests, employees
from ..models.request import RequestStatus

client = TestClient(app)

def test_create_request(test_db: Session, test_token: str):
    request_data = {
        "title": "Test Request",
        "description": "Test Description",
        "priority": "low",
        "status": "new"
    }
    
    response = client.post(
        "/api/requests/",
        json=request_data,
        headers={"Authorization": f"Bearer {test_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == request_data["title"]
    assert data["description"] == request_data["description"]
    assert data["priority"] == request_data["priority"]
    assert data["status"] == RequestStatus.NEW.value

def test_create_request_unauthorized():
    request_data = {
        "title": "Test Request",
        "description": "Test Description",
        "priority": "low"
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
                "title": f"Test Request {i}",
                "description": f"Test Description {i}",
                "priority": "low",
                "status": "new"
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
    # Создаем тестовую заявку
    employee = employees.create_employee(
        test_db,
        {
            "first_name": "Test",
            "last_name": "User",
            "department": "IT",
            "office": "101",
            "password": "testpass123"
        }
    )
    
    request = requests.create_request(
        test_db,
        {
            "title": "Test Request",
            "description": "Test Description",
            "priority": "low",
            "status": "new"
        },
        employee.id
    )
    
    response = client.put(
        f"/api/requests/{request.id}",
        json={"status": "in_progress"},
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
    assert "total" in data
    assert "new" in data
    assert "in_progress" in data
    assert "completed" in data
    assert "rejected" in data 