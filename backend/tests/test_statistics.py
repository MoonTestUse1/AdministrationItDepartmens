from fastapi.testclient import TestClient
import pytest
from app.core.auth import create_access_token

def test_get_statistics_admin(client: TestClient, test_admin: dict):
    """Test getting statistics as admin"""
    access_token = create_access_token(
        data={"sub": test_admin["email"], "is_admin": True}
    )
    
    response = client.get(
        "/api/admin/statistics",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "total_requests" in data
    assert "total_users" in data
    assert "status_stats" in data
    assert "daily_stats" in data

def test_get_statistics_not_admin(client: TestClient, test_user: dict):
    """Test getting statistics without admin rights"""
    access_token = create_access_token(
        data={"sub": test_user["email"], "is_admin": False}
    )
    
    response = client.get(
        "/api/admin/statistics",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 403

def test_get_statistics_no_auth(client: TestClient):
    """Test getting statistics without authentication"""
    response = client.get("/api/admin/statistics")
    assert response.status_code == 401 