"""Employee tests."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.employee import Employee

def test_create_employee(client: TestClient, admin_token: str, db: Session):
    """Тест создания сотрудника."""
    response = client.post(
        "/api/employees",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "email": "new@example.com",
            "password": "newpassword",
            "full_name": "New Employee",
            "department": "IT",
            "is_active": True,
            "is_admin": False
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "new@example.com"
    assert data["full_name"] == "New Employee"
    assert data["department"] == "IT"
    assert "id" in data

def test_create_employee_unauthorized(client: TestClient):
    """Тест создания сотрудника без авторизации."""
    response = client.post(
        "/api/employees",
        json={
            "email": "new@example.com",
            "password": "newpassword",
            "full_name": "New Employee",
            "is_active": True,
            "is_admin": False
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_get_employees(client: TestClient, admin_token: str, test_employee: Employee, db: Session):
    """Тест получения списка сотрудников."""
    response = client.get(
        "/api/employees",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "email" in data[0]
    assert "full_name" in data[0]
    assert "department" in data[0]

def test_get_employee_by_id(client: TestClient, admin_token: str, test_employee: Employee, db: Session):
    """Тест получения сотрудника по ID."""
    response = client.get(
        f"/api/employees/{test_employee.id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_employee.email
    assert data["full_name"] == test_employee.full_name
    assert data["department"] == test_employee.department

def test_get_nonexistent_employee(client: TestClient, admin_token: str):
    """Тест получения несуществующего сотрудника."""
    response = client.get(
        "/api/employees/999",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Employee not found"

def test_update_employee(client: TestClient, admin_token: str, test_employee: Employee, db: Session):
    """Тест обновления данных сотрудника."""
    response = client.put(
        f"/api/employees/{test_employee.id}",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "email": "updated@example.com",
            "full_name": "Updated Employee",
            "department": "HR",
            "is_active": True,
            "is_admin": False
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "updated@example.com"
    assert data["full_name"] == "Updated Employee"
    assert data["department"] == "HR"

def test_delete_employee(client: TestClient, admin_token: str, test_employee: Employee, db: Session):
    """Тест удаления сотрудника."""
    response = client.delete(
        f"/api/employees/{test_employee.id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_employee.email
    assert data["full_name"] == test_employee.full_name
    assert data["department"] == test_employee.department

def test_employee_me(client: TestClient, employee_token: str, test_employee: Employee, db: Session):
    """Тест получения информации о текущем сотруднике."""
    response = client.get(
        "/api/employees/me",
        headers={"Authorization": f"Bearer {employee_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_employee.email
    assert data["full_name"] == test_employee.full_name
    assert data["department"] == test_employee.department

def test_update_me(client: TestClient, employee_token: str, test_employee: Employee, db: Session):
    """Тест обновления информации о текущем сотруднике."""
    response = client.put(
        "/api/employees/me",
        headers={"Authorization": f"Bearer {employee_token}"},
        json={
            "full_name": "Updated Name",
            "department": "Support"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"
    assert data["email"] == test_employee.email
    assert data["department"] == "Support" 