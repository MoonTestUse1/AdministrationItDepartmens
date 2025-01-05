"""Authentication tests."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.employee import Employee

def test_login_employee_success(client: TestClient, test_employee: Employee):
    """Тест успешной авторизации сотрудника."""
    response = client.post(
        "/api/auth/login",
        data={"username": test_employee.email, "password": "testpassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_employee_wrong_password(client: TestClient, test_employee: Employee):
    """Тест авторизации сотрудника с неверным паролем."""
    response = client.post(
        "/api/auth/login",
        data={"username": test_employee.email, "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

def test_login_employee_wrong_username(client: TestClient):
    """Тест авторизации с несуществующим пользователем."""
    response = client.post(
        "/api/auth/login",
        data={"username": "nonexistent@example.com", "password": "testpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

def test_login_admin_success(client: TestClient, test_admin: Employee):
    """Тест успешной авторизации администратора."""
    response = client.post(
        "/api/auth/admin/login",
        data={"username": test_admin.email, "password": "adminpassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_admin_wrong_password(client: TestClient, test_admin: Employee):
    """Тест авторизации администратора с неверным паролем."""
    response = client.post(
        "/api/auth/admin/login",
        data={"username": test_admin.email, "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

def test_protected_route_with_valid_token(client: TestClient, employee_token: str, test_employee: Employee, db: Session):
    """Тест доступа к защищенному маршруту с валидным токеном."""
    response = client.get(
        "/api/employees/me",
        headers={"Authorization": f"Bearer {employee_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_employee.email
    assert data["full_name"] == test_employee.full_name

def test_protected_route_without_token(client: TestClient):
    """Тест доступа к защищенному маршруту без токена."""
    response = client.get("/api/employees/me")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_protected_route_with_invalid_token(client: TestClient):
    """Тест доступа к защищенному маршруту с недействительным токеном."""
    response = client.get(
        "/api/employees/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials" 