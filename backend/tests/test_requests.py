"""Request tests"""
from fastapi.testclient import TestClient

def test_create_request(client: TestClient, employee_headers):
    """Test create request"""
    response = client.post(
        "/api/requests/",
        headers=employee_headers,
        json={
            "request_type": "HARDWARE",
            "description": "Need new laptop",
            "priority": "HIGH"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["request_type"] == "HARDWARE"
    assert data["description"] == "Need new laptop"
    assert data["priority"] == "HIGH"
    assert data["status"] == "NEW"

def test_get_my_requests(client: TestClient, employee_headers):
    """Test get my requests"""
    response = client.get("/api/requests/my", headers=employee_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_all_requests_admin(client: TestClient, admin_headers):
    """Test get all requests as admin"""
    response = client.get("/api/requests/", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_all_requests_not_admin(client: TestClient, employee_headers):
    """Test get all requests without admin rights"""
    response = client.get("/api/requests/", headers=employee_headers)
    assert response.status_code == 403

def test_update_request_status_admin(client: TestClient, admin_headers):
    """Test update request status as admin"""
    # Сначала создаем запрос
    create_response = client.post(
        "/api/requests/",
        headers=admin_headers,
        json={
            "request_type": "SOFTWARE",
            "description": "Need new IDE",
            "priority": "MEDIUM"
        }
    )
    request_id = create_response.json()["id"]
    
    # Затем обновляем его статус
    response = client.put(
        f"/api/requests/{request_id}/status",
        headers=admin_headers,
        json={"status": "IN_PROGRESS"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "IN_PROGRESS"

def test_update_request_status_not_admin(client: TestClient, employee_headers):
    """Test update request status without admin rights"""
    response = client.put(
        "/api/requests/1/status",
        headers=employee_headers,
        json={"status": "IN_PROGRESS"}
    )
    assert response.status_code == 403 