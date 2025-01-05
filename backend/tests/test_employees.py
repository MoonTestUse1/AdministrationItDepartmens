"""Employee tests."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.auth import create_access_token
from app.models.user import User

pytestmark = pytest.mark.asyncio

@pytest.mark.asyncio
async def test_create_employee(client: TestClient, test_admin: dict, db: Session):
    """Test creating a new employee."""
    access_token = create_access_token(
        data={"sub": test_admin["email"], "is_admin": True}
    )
    
    employee_data = {
        "email": "new@example.com",
        "password": "newpass123",
        "full_name": "New Employee",
        "is_admin": False
    }
    
    response = client.post(
        "/api/employees/",
        headers={"Authorization": f"Bearer {access_token}"},
        json=employee_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == employee_data["email"]
    assert data["full_name"] == employee_data["full_name"]
    assert not data["is_admin"]

@pytest.mark.asyncio
async def test_create_employee_unauthorized(client: TestClient, test_user: dict):
    """Test creating an employee without admin rights."""
    access_token = create_access_token(
        data={"sub": test_user["email"], "is_admin": False}
    )
    
    employee_data = {
        "email": "new@example.com",
        "password": "newpass123",
        "full_name": "New Employee",
        "is_admin": False
    }
    
    response = client.post(
        "/api/employees/",
        headers={"Authorization": f"Bearer {access_token}"},
        json=employee_data
    )
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_get_employee(client: TestClient, test_admin: dict, test_user: dict, db: Session):
    """Test getting an employee by ID."""
    access_token = create_access_token(
        data={"sub": test_admin["email"], "is_admin": True}
    )
    
    # Получаем ID тестового пользователя
    user = db.query(User).filter(User.email == test_user["email"]).first()
    
    response = client.get(
        f"/api/employees/{user.id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user["email"]
    assert data["full_name"] == test_user["full_name"]

@pytest.mark.asyncio
async def test_update_employee_me(client: TestClient, test_user: dict):
    """Test updating current employee info."""
    access_token = create_access_token(
        data={"sub": test_user["email"], "is_admin": False}
    )
    
    update_data = {
        "full_name": "Updated Name"
    }
    
    response = client.put(
        "/api/employees/me",
        headers={"Authorization": f"Bearer {access_token}"},
        json=update_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == update_data["full_name"] 