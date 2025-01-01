import pytest
from app.models.employee import Employee
from app.utils.auth import get_password_hash

def test_create_employee(client):
    """Test creating a new employee"""
    # Login as admin
    admin_response = client.post("/api/auth/admin", json={
        "username": "admin",
        "password": "admin123"
    })
    assert admin_response.status_code == 200
    admin_token = admin_response.json()["access_token"]

    # Create employee
    employee_data = {
        "first_name": "John",
        "last_name": "Doe",
        "department": "IT",
        "office": "B205",
        "password": "test123"
    }
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.post("/api/employees/", json=employee_data, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == employee_data["first_name"]
    assert data["last_name"] == employee_data["last_name"]
    assert data["department"] == employee_data["department"]
    assert data["office"] == employee_data["office"]
    assert "password" not in data

def test_get_employees(client, db_session):
    """Test getting list of employees"""
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
    
    # Сохраняем значения для проверки
    expected_first_name = employee.first_name
    expected_last_name = employee.last_name
    expected_department = employee.department
    expected_office = employee.office
    
    # Login as admin
    admin_response = client.post("/api/auth/admin", json={
        "username": "admin",
        "password": "admin123"
    })
    assert admin_response.status_code == 200
    admin_token = admin_response.json()["access_token"]
    
    # Get employees list
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/api/employees/", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["first_name"] == expected_first_name
    assert data[0]["last_name"] == expected_last_name
    assert data[0]["department"] == expected_department
    assert data[0]["office"] == expected_office
    assert "password" not in data[0]

def test_create_employee_unauthorized(client):
    """Test creating employee without authorization"""
    employee_data = {
        "first_name": "John",
        "last_name": "Doe",
        "department": "IT",
        "office": "B205",
        "password": "test123"
    }
    response = client.post("/api/employees/", json=employee_data)
    assert response.status_code == 401

def test_get_employees_unauthorized(client):
    """Test getting employees list without authorization"""
    response = client.get("/api/employees/")
    assert response.status_code == 401

def test_get_employee_by_id(client, db_session):
    """Test getting employee by ID"""
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
    
    # Login as admin
    admin_response = client.post("/api/auth/admin", json={
        "username": "admin",
        "password": "admin123"
    })
    assert admin_response.status_code == 200
    admin_token = admin_response.json()["access_token"]
    
    # Get employee
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get(f"/api/employees/{employee_id}", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Test"
    assert data["last_name"] == "User"
    assert data["department"] == "IT"
    assert data["office"] == "A101"
    assert "password" not in data

def test_update_employee(client, db_session):
    """Test updating employee data"""
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
    
    # Login as admin
    admin_response = client.post("/api/auth/admin", json={
        "username": "admin",
        "password": "admin123"
    })
    assert admin_response.status_code == 200
    admin_token = admin_response.json()["access_token"]
    
    # Update employee
    update_data = {
        "first_name": "Updated",
        "last_name": "Name",
        "department": "HR",
        "office": "B202"
    }
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.put(f"/api/employees/{employee_id}", json=update_data, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == update_data["first_name"]
    assert data["last_name"] == update_data["last_name"]
    assert data["department"] == update_data["department"]
    assert data["office"] == update_data["office"]
    assert "password" not in data

def test_delete_employee(client, db_session):
    """Test deleting employee"""
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
    
    # Login as admin
    admin_response = client.post("/api/auth/admin", json={
        "username": "admin",
        "password": "admin123"
    })
    assert admin_response.status_code == 200
    admin_token = admin_response.json()["access_token"]
    
    # Delete employee
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.delete(f"/api/employees/{employee_id}", headers=headers)
    
    assert response.status_code == 200
    
    # Verify employee is deleted
    get_response = client.get(f"/api/employees/{employee_id}", headers=headers)
    assert get_response.status_code == 404 