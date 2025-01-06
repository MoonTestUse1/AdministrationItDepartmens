"""Request tests"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

def test_create_request(client: TestClient, employee_token: str):
    """Test request creation"""
    response = client.post(
        "/api/requests",
        headers={"Authorization": f"Bearer {employee_token}"},
        json={
            "request_type": "equipment",
            "description": "Need a new laptop",
            "priority": "medium"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["request_type"] == "equipment"
    assert data["description"] == "Need a new laptop"
    assert data["priority"] == "medium"
    assert data["status"] == "new"

def test_create_request_unauthorized(client: TestClient):
    """Test request creation without authorization"""
    response = client.post(
        "/api/requests",
        json={
            "request_type": "equipment",
            "description": "Need a new laptop",
            "priority": "medium"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_get_my_requests(client: TestClient, employee_token: str):
    """Test getting employee's requests"""
    response = client.get(
        "/api/requests/my",
        headers={"Authorization": f"Bearer {employee_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_my_requests_unauthorized(client: TestClient):
    """Test getting employee's requests without authorization"""
    response = client.get("/api/requests/my")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_get_all_requests_admin(client: TestClient, admin_token: str):
    """Test getting all requests by admin"""
    response = client.get(
        "/api/requests/admin",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_all_requests_unauthorized(client: TestClient):
    """Test getting all requests without authorization"""
    response = client.get("/api/requests/admin")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_get_all_requests_not_admin(client: TestClient, employee_token: str):
    """Test getting all requests by non-admin user"""
    response = client.get(
        "/api/requests/admin",
        headers={"Authorization": f"Bearer {employee_token}"}
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Not enough permissions"

def test_update_request_status_admin(client: TestClient, admin_token: str):
    """Test updating request status by admin"""
    # Сначала создаем запрос
    response = client.post(
        "/api/requests",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "request_type": "equipment",
            "description": "Need a new laptop",
            "priority": "medium"
        }
    )
    request_id = response.json()["id"]

    # Обновляем статус
    response = client.patch(
        f"/api/requests/{request_id}/status",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"status": "in_progress"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "in_progress"

def test_update_request_status_not_admin(client: TestClient, employee_token: str):
    """Test updating request status by non-admin user"""
    response = client.patch(
        "/api/requests/1/status",
        headers={"Authorization": f"Bearer {employee_token}"},
        json={"status": "in_progress"}
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Not enough permissions"

def test_update_request_status_unauthorized(client: TestClient):
    """Test updating request status without authorization"""
    response = client.patch(
        "/api/requests/1/status",
        json={"status": "in_progress"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated" 