import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.crud import employees
from app.utils.auth import verify_password, get_password_hash
from app.schemas.employee import EmployeeCreate
from app.core.auth import create_access_token
from app.core.redis import redis_client

client = TestClient(app)

# Переопределяем redis_client для тестов
def pytest_configure(config):
    from app.core import redis
    redis.redis_client = config.getoption("--redis", default=None)

pytestmark = pytest.mark.asyncio

@pytest.mark.asyncio
async def test_login_success(client: TestClient, test_user: dict, redis):
    """Test successful login"""
    response = client.post(
        "/api/auth/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_wrong_password(client: TestClient, test_user: dict, redis):
    """Test login with wrong password"""
    response = client.post(
        "/api/auth/login",
        data={
            "username": test_user["email"],
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

@pytest.mark.asyncio
async def test_login_wrong_email(client: TestClient, redis):
    """Test login with wrong email"""
    response = client.post(
        "/api/auth/login",
        data={
            "username": "wrong@example.com",
            "password": "test123"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

@pytest.mark.asyncio
async def test_get_current_user(client: TestClient, test_user: dict, redis):
    """Test getting current user info"""
    access_token = create_access_token(
        data={"sub": test_user["email"], "is_admin": False}
    )
    
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == test_user["email"]
    assert response.json()["full_name"] == test_user["full_name"]
    assert not response.json()["is_admin"]

@pytest.mark.asyncio
async def test_get_current_user_no_token(client: TestClient, redis):
    """Test getting current user without token"""
    response = client.get("/api/auth/me")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

@pytest.mark.asyncio
async def test_get_current_user_invalid_token(client: TestClient, redis):
    """Test getting current user with invalid token"""
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials" 