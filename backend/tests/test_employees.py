"""Employee tests"""
from fastapi.testclient import TestClient

def test_create_employee(client: TestClient, admin_headers):
    """Test create employee"""
    response = client.post(
        "/api/employees/",
        headers=admin_headers,
        json={
            "first_name": "New",
            "last_name": "Employee",
            "department": "IT",
            "office": "Main",
            "password": "newpass123",
            "is_active": True,
            "is_admin": False
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "New"
    assert data["last_name"] == "Employee"
    assert "hashed_password" not in data

def test_create_employee_not_admin(client: TestClient, employee_headers):
    """Test create employee without admin rights"""
    response = client.post(
        "/api/employees/",
        headers=employee_headers,
        json={
            "first_name": "New",
            "last_name": "Employee",
            "department": "IT",
            "office": "Main",
            "password": "newpass123",
            "is_active": True,
            "is_admin": False
        }
    )
    assert response.status_code == 403

def test_get_employees(client: TestClient, admin_headers):
    """Test get all employees"""
    response = client.get("/api/employees/", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_employees_not_admin(client: TestClient, employee_headers):
    """Test get all employees without admin rights"""
    response = client.get("/api/employees/", headers=employee_headers)
    assert response.status_code == 403

def test_get_me(client: TestClient, employee_headers, test_employee):
    """Test get current employee"""
    response = client.get("/api/employees/me", headers=employee_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_employee.id
    assert data["first_name"] == test_employee.first_name
    assert data["last_name"] == test_employee.last_name

def test_update_me(client: TestClient, employee_headers, test_employee):
    """Test update current employee"""
    response = client.put(
        "/api/employees/me",
        headers=employee_headers,
        json={
            "first_name": "Updated",
            "last_name": "User",
            "department": "HR",
            "office": "Branch"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Updated"
    assert data["last_name"] == "User"
    assert data["department"] == "HR"
    assert data["office"] == "Branch" 