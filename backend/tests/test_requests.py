import pytest
from app.models.request import Request, RequestStatus, RequestPriority
from app.models.employee import Employee
from app.utils.auth import get_password_hash
from datetime import datetime, timedelta

def test_create_request(client, db_session):
    """Test creating a new request"""
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
    employee_id = employee.id

    # Login as employee
    login_response = client.post("/api/auth/login", json={
        "last_name": "User",
        "password": "test123"
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Create request
    request_data = {
        "title": "Test Request",
        "description": "This is a test request",
        "priority": RequestPriority.MEDIUM.value
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/api/requests/", json=request_data, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == request_data["title"]
    assert data["description"] == request_data["description"]
    assert data["priority"] == request_data["priority"]
    assert data["status"] == RequestStatus.NEW.value
    assert data["employee_id"] == employee_id

def test_get_employee_requests(client, db_session):
    """Test getting employee's requests"""
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
    employee_id = employee.id

    # Create test request and save its data
    request = Request(
        title="Test Request",
        description="This is a test request",
        priority=RequestPriority.MEDIUM.value,
        status=RequestStatus.NEW.value,
        employee_id=employee_id
    )
    db_session.add(request)
    db_session.commit()
    
    # Сохраняем данные для сравнения
    expected_data = {
        "title": request.title,
        "description": request.description,
        "priority": request.priority,
        "status": request.status,
        "employee_id": request.employee_id
    }

    # Login as employee
    login_response = client.post("/api/auth/login", json={
        "last_name": "User",
        "password": "test123"
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Get requests
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/requests/my", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == expected_data["title"]
    assert data[0]["description"] == expected_data["description"]
    assert data[0]["priority"] == expected_data["priority"]
    assert data[0]["status"] == expected_data["status"]
    assert data[0]["employee_id"] == expected_data["employee_id"]

def test_update_request_status(client, db_session):
    """Test updating request status"""
    # Create test employee and request
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
    employee_id = employee.id

    request = Request(
        title="Test Request",
        description="This is a test request",
        priority=RequestPriority.MEDIUM.value,
        status=RequestStatus.NEW.value,
        employee_id=employee_id
    )
    db_session.add(request)
    db_session.commit()
    request_id = request.id

    # Login as admin
    admin_response = client.post("/api/auth/admin", json={
        "username": "admin",
        "password": "admin123"
    })
    assert admin_response.status_code == 200
    admin_token = admin_response.json()["access_token"]

    # Update request status
    update_data = {"status": RequestStatus.IN_PROGRESS.value}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.patch(f"/api/requests/{request_id}/status", json=update_data, headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == RequestStatus.IN_PROGRESS.value

def test_get_all_requests_admin(client, db_session):
    """Test getting all requests as admin"""
    # Create test employees and requests
    hashed_password = get_password_hash("test123")
    employee1 = Employee(
        first_name="Test1",
        last_name="User1",
        department="IT",
        office="A101",
        password=hashed_password
    )
    employee2 = Employee(
        first_name="Test2",
        last_name="User2",
        department="HR",
        office="B202",
        password=hashed_password
    )
    db_session.add_all([employee1, employee2])
    db_session.commit()

    request1 = Request(
        title="Test Request 1",
        description="This is test request 1",
        priority=RequestPriority.HIGH.value,
        status=RequestStatus.NEW.value,
        employee_id=employee1.id
    )
    request2 = Request(
        title="Test Request 2",
        description="This is test request 2",
        priority=RequestPriority.MEDIUM.value,
        status=RequestStatus.IN_PROGRESS.value,
        employee_id=employee2.id
    )
    db_session.add_all([request1, request2])
    db_session.commit()
    
    # Сохраняем данные для сравнения
    expected_titles = {request1.title, request2.title}

    # Login as admin
    admin_response = client.post("/api/auth/admin", json={
        "username": "admin",
        "password": "admin123"
    })
    assert admin_response.status_code == 200
    admin_token = admin_response.json()["access_token"]

    # Get all requests
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/api/requests/admin", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    received_titles = {r["title"] for r in data}
    assert received_titles == expected_titles

def test_get_requests_by_status(client, db_session):
    """Test filtering requests by status"""
    # Create test employee and requests
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

    request1 = Request(
        title="New Request",
        description="This is a new request",
        priority=RequestPriority.HIGH.value,
        status=RequestStatus.NEW.value,
        employee_id=employee.id
    )
    request2 = Request(
        title="In Progress Request",
        description="This is an in progress request",
        priority=RequestPriority.MEDIUM.value,
        status=RequestStatus.IN_PROGRESS.value,
        employee_id=employee.id
    )
    db_session.add_all([request1, request2])
    db_session.commit()
    
    # Сохраняем данные для сравнения
    expected_data = {
        "title": request1.title,
        "status": request1.status
    }

    # Login as admin
    admin_response = client.post("/api/auth/admin", json={
        "username": "admin",
        "password": "admin123"
    })
    assert admin_response.status_code == 200
    admin_token = admin_response.json()["access_token"]

    # Get requests filtered by status
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get(f"/api/requests/admin?status={RequestStatus.NEW.value}", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == expected_data["title"]
    assert data[0]["status"] == expected_data["status"]

def test_get_request_statistics(client, db_session):
    """Test getting request statistics"""
    # Create test employee and requests
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

    # Create requests with different statuses
    requests_data = [
        {"status": RequestStatus.NEW.value, "priority": RequestPriority.HIGH.value},
        {"status": RequestStatus.IN_PROGRESS.value, "priority": RequestPriority.MEDIUM.value},
        {"status": RequestStatus.COMPLETED.value, "priority": RequestPriority.LOW.value},
        {"status": RequestStatus.NEW.value, "priority": RequestPriority.HIGH.value}
    ]

    for i, data in enumerate(requests_data):
        request = Request(
            title=f"Request {i+1}",
            description=f"This is request {i+1}",
            priority=data["priority"],
            status=data["status"],
            employee_id=employee.id
        )
        db_session.add(request)
    db_session.commit()

    # Login as admin
    admin_response = client.post("/api/auth/admin", json={
        "username": "admin",
        "password": "admin123"
    })
    assert admin_response.status_code == 200
    admin_token = admin_response.json()["access_token"]

    # Get statistics
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/api/requests/statistics", headers=headers)

    assert response.status_code == 200
    data = response.json()
    
    # Проверяем статистику
    assert "total_requests" in data
    assert data["total_requests"] == 4
    assert "by_status" in data
    assert data["by_status"]["new"] == 2
    assert data["by_status"]["in_progress"] == 1
    assert data["by_status"]["completed"] == 1
    assert "by_priority" in data
    assert data["by_priority"]["high"] == 2
    assert data["by_priority"]["medium"] == 1
    assert data["by_priority"]["low"] == 1

def test_create_request_unauthorized(client):
    """Test creating request without authorization"""
    request_data = {
        "title": "Test Request",
        "description": "This is a test request",
        "priority": RequestPriority.MEDIUM.value
    }
    response = client.post("/api/requests/", json=request_data)
    assert response.status_code == 401

def test_get_requests_unauthorized(client):
    """Test getting requests without authorization"""
    response = client.get("/api/requests/my")
    assert response.status_code == 401 