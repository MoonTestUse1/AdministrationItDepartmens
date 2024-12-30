"""Request management endpoint tests"""
import pytest
from unittest.mock import patch

def test_create_request(client, test_db, test_employee, test_request):
    """Test request creation"""
    # Create test employee first
    employee_response = client.post(
        "/api/employees",
        json={
            "first_name": test_employee["first_name"],
            "last_name": test_employee["last_name"],
            "department": test_employee["department"],
            "office": test_employee["office"],
            "password": test_employee["password"]
        }
    )
    assert employee_response.status_code == 200
    employee_data = employee_response.json()
    test_request["employee_id"] = employee_data["id"]
    
    # Create request
    with patch('app.bot.notifications.send_notification'):  # Mock notification
        response = client.post(
            "/api/requests",
            json=test_request
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["employee_id"] == test_request["employee_id"]
    assert data["status"] == "new"

def test_create_request_invalid_employee(client, test_request):
    """Test creating request with invalid employee ID"""
    test_request["employee_id"] = 999  # Non-existent ID
    
    response = client.post(
        "/api/requests",
        json=test_request
    )
    
    assert response.status_code == 404
    assert "не найден" in response.json()["detail"]

def test_create_request_invalid_priority(client, test_db, test_employee):
    """Test creating request with invalid priority"""
    # Create test employee first
    employee_response = client.post(
        "/api/employees",
        json={
            "first_name": test_employee["first_name"],
            "last_name": test_employee["last_name"],
            "department": test_employee["department"],
            "office": test_employee["office"],
            "password": test_employee["password"]
        }
    )
    assert employee_response.status_code == 200
    employee_data = employee_response.json()
    
    invalid_request = {
        "employee_id": employee_data["id"],
        "department": "general",
        "request_type": "hardware",
        "priority": "invalid",  # Invalid priority
        "description": "Test request"
    }
    
    response = client.post(
        "/api/requests",
        json=invalid_request
    )
    
    assert response.status_code == 422