import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.models.request import RequestStatus, RequestPriority
from app.crud import requests
from app.schemas.request import RequestCreate

client = TestClient(app)

def test_create_request(test_db: Session, test_employee, test_auth_header):
    """Test creating a new request"""
    request_data = {
        "department": "IT",
        "request_type": "hardware",
        "description": "This is a test request",
        "priority": RequestPriority.MEDIUM.value
    }
    
    response = client.post(
        "/api/requests/",
        json=request_data,
        headers=test_auth_header
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["department"] == request_data["department"]
    assert data["description"] == request_data["description"]
    assert data["priority"] == request_data["priority"]
    assert data["status"] == RequestStatus.NEW.value
    assert "employee_id" in data

def test_get_employee_requests(test_db: Session, test_employee, test_auth_header):
    """Test getting employee's requests"""
    # Создаем тестовую заявку
    request_data = RequestCreate(
        department="IT",
        request_type="hardware",
        description="This is a test request",
        priority=RequestPriority.MEDIUM.value
    )
    test_request = requests.create_request(test_db, request_data, test_employee.id)
    
    response = client.get("/api/requests/my", headers=test_auth_header)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["department"] == test_request.department
    assert data[0]["description"] == test_request.description
    assert data[0]["priority"] == test_request.priority
    assert data[0]["status"] == test_request.status
    assert data[0]["employee_id"] == test_request.employee_id

def test_update_request_status(test_db: Session, test_employee, admin_auth_header):
    """Test updating request status"""
    # Создаем тестовую заявку
    request_data = RequestCreate(
        department="IT",
        request_type="hardware",
        description="This is a test request",
        priority=RequestPriority.MEDIUM.value
    )
    test_request = requests.create_request(test_db, request_data, test_employee.id)
    
    update_data = {"status": RequestStatus.IN_PROGRESS.value}
    response = client.patch(
        f"/api/requests/{test_request.id}/status",
        json=update_data,
        headers=admin_auth_header
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == RequestStatus.IN_PROGRESS.value

def test_get_all_requests_admin(test_db: Session, test_employee, admin_auth_header):
    """Test getting all requests as admin"""
    # Создаем тестовую заявку
    request_data = RequestCreate(
        department="IT",
        request_type="hardware",
        description="This is a test request",
        priority=RequestPriority.MEDIUM.value
    )
    test_request = requests.create_request(test_db, request_data, test_employee.id)
    
    response = client.get("/api/requests/admin", headers=admin_auth_header)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["department"] == test_request.department

def test_get_requests_by_status(test_db: Session, test_employee, admin_auth_header):
    """Test filtering requests by status"""
    # Создаем тестовую заявку
    request_data = RequestCreate(
        department="IT",
        request_type="hardware",
        description="This is a test request",
        priority=RequestPriority.MEDIUM.value
    )
    test_request = requests.create_request(test_db, request_data, test_employee.id)
    
    response = client.get(
        f"/api/requests/admin?status={RequestStatus.NEW.value}",
        headers=admin_auth_header
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["status"] == RequestStatus.NEW.value

def test_get_request_statistics(test_db: Session, test_employee, admin_auth_header):
    """Test getting request statistics"""
    # Создаем тестовые заявки с разными статусами
    requests_data = [
        RequestCreate(
            department="IT",
            request_type="hardware",
            description="Test request 1",
            priority=RequestPriority.HIGH.value
        ),
        RequestCreate(
            department="IT",
            request_type="software",
            description="Test request 2",
            priority=RequestPriority.MEDIUM.value
        )
    ]
    
    for data in requests_data:
        requests.create_request(test_db, data, test_employee.id)
    
    response = client.get("/api/requests/statistics", headers=admin_auth_header)
    
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "by_status" in data
    assert data["total"] == 2
    assert data["by_status"][RequestStatus.NEW.value] == 2
    assert data["by_status"][RequestStatus.IN_PROGRESS.value] == 0
    assert data["by_status"][RequestStatus.COMPLETED.value] == 0
    assert data["by_status"][RequestStatus.REJECTED.value] == 0

def test_create_request_unauthorized(test_db: Session):
    """Test creating request without authorization"""
    request_data = {
        "department": "IT",
        "request_type": "hardware",
        "description": "This is a test request",
        "priority": RequestPriority.MEDIUM.value
    }
    response = client.post("/api/requests/", json=request_data)
    assert response.status_code == 401

def test_get_requests_unauthorized(test_db: Session):
    """Test getting requests without authorization"""
    response = client.get("/api/requests/my")
    assert response.status_code == 401 