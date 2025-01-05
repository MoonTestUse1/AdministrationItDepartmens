import pytest
from fastapi.testclient import TestClient
from app.core.auth import create_access_token

pytestmark = pytest.mark.asyncio

@pytest.mark.asyncio
async def test_create_request(client: TestClient, test_user: dict, redis):
    """Test creating a new request"""
    access_token = create_access_token(
        data={"sub": test_user["email"], "is_admin": False}
    )
    
    request_data = {
        "request_type": "technical",
        "description": "Test request",
        "priority": "medium"
    }
    
    response = client.post(
        "/api/requests/",
        headers={"Authorization": f"Bearer {access_token}"},
        json=request_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["request_type"] == request_data["request_type"]
    assert data["description"] == request_data["description"]
    assert data["priority"] == request_data["priority"]
    assert data["status"] == "new"

@pytest.mark.asyncio
async def test_create_request_invalid_priority(client: TestClient, test_user: dict, redis):
    """Test creating a request with invalid priority"""
    access_token = create_access_token(
        data={"sub": test_user["email"], "is_admin": False}
    )
    
    request_data = {
        "request_type": "technical",
        "description": "Test request",
        "priority": "invalid"
    }
    
    response = client.post(
        "/api/requests/",
        headers={"Authorization": f"Bearer {access_token}"},
        json=request_data
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_get_user_requests(client: TestClient, test_user: dict, redis):
    """Test getting user's requests"""
    access_token = create_access_token(
        data={"sub": test_user["email"], "is_admin": False}
    )
    
    response = client.get(
        "/api/requests/my",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_update_request_status(client: TestClient, test_admin: dict, redis):
    """Test updating request status (admin only)"""
    access_token = create_access_token(
        data={"sub": test_admin["email"], "is_admin": True}
    )
    
    # Сначала создаем запрос
    request_data = {
        "request_type": "technical",
        "description": "Test request",
        "priority": "medium"
    }
    
    create_response = client.post(
        "/api/requests/",
        headers={"Authorization": f"Bearer {access_token}"},
        json=request_data
    )
    request_id = create_response.json()["id"]
    
    # Теперь обновляем статус
    update_data = {
        "status": "in_progress"
    }
    
    response = client.put(
        f"/api/admin/requests/{request_id}/status",
        headers={"Authorization": f"Bearer {access_token}"},
        json=update_data
    )
    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"

@pytest.mark.asyncio
async def test_update_request_status_not_admin(client: TestClient, test_user: dict, redis):
    """Test updating request status without admin rights"""
    access_token = create_access_token(
        data={"sub": test_user["email"], "is_admin": False}
    )
    
    update_data = {
        "status": "in_progress"
    }
    
    response = client.put(
        "/api/admin/requests/1/status",
        headers={"Authorization": f"Bearer {access_token}"},
        json=update_data
    )
    assert response.status_code == 403 