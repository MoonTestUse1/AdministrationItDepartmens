"""Request tests."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.employee import Employee
from app.models.request import Request

def test_create_request(client: TestClient, employee_token: str, db: Session):
    """Тест создания заявки."""
    response = client.post(
        "/api/requests",
        headers={"Authorization": f"Bearer {employee_token}"},
        json={
            "request_type": "equipment",
            "description": "Test Description",
            "priority": "medium"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["request_type"] == "equipment"
    assert data["description"] == "Test Description"
    assert data["priority"] == "medium"
    assert data["status"] == "new"
    assert "id" in data

def test_create_request_unauthorized(client: TestClient):
    """Тест создания заявки без авторизации."""
    response = client.post(
        "/api/requests",
        json={
            "request_type": "equipment",
            "description": "Test Description",
            "priority": "medium"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_get_employee_requests(client: TestClient, employee_token: str, test_employee: Employee, db: Session):
    """Тест получения списка заявок сотрудника."""
    # Создаем тестовую заявку
    request = Request(
        request_type="equipment",
        description="Test Description",
        priority="medium",
        status="new",
        employee_id=test_employee.id
    )
    db.add(request)
    db.commit()

    response = client.get(
        "/api/requests/my",
        headers={"Authorization": f"Bearer {employee_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["request_type"] == "equipment"
    assert data[0]["description"] == "Test Description"

def test_admin_get_all_requests(client: TestClient, admin_token: str, test_employee: Employee, db: Session):
    """Тест получения всех заявок администратором."""
    # Создаем тестовую заявку
    request = Request(
        request_type="equipment",
        description="Test Description",
        priority="medium",
        status="new",
        employee_id=test_employee.id
    )
    db.add(request)
    db.commit()

    response = client.get(
        "/api/requests/admin",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["request_type"] == "equipment"
    assert data[0]["description"] == "Test Description"

def test_update_request_status(client: TestClient, admin_token: str, test_employee: Employee, db: Session):
    """Тест обновления статуса заявки."""
    # Создаем тестовую заявку
    request = Request(
        request_type="equipment",
        description="Test Description",
        priority="medium",
        status="new",
        employee_id=test_employee.id
    )
    db.add(request)
    db.commit()

    response = client.patch(
        f"/api/requests/{request.id}/status",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"status": "in_progress"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "in_progress"

def test_get_request_statistics(client: TestClient, admin_token: str, test_employee: Employee, db: Session):
    """Тест получения статистики по заявкам."""
    # Создаем тестовые заявки с разными статусами
    requests = [
        Request(
            request_type="equipment",
            description="Test Description",
            priority="medium",
            status="new",
            employee_id=test_employee.id
        ),
        Request(
            request_type="equipment",
            description="Test Description",
            priority="high",
            status="in_progress",
            employee_id=test_employee.id
        ),
        Request(
            request_type="equipment",
            description="Test Description",
            priority="low",
            status="completed",
            employee_id=test_employee.id
        )
    ]
    for req in requests:
        db.add(req)
    db.commit()

    response = client.get(
        "/api/statistics",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "by_status" in data
    assert data["total"] >= 3 