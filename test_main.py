from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def authenticate_as_admin():
    response = client.post(
        "/auth/token",
        data={"username": "fakemail@fmail.com", "password": "admin"},
    )
    return response.json()["access_token"]

#region TEST: CRUD ENDPOINTS

#region TEST: CREATE

def test_create_user():
    user_data = {
        "email": "test@example.com",
        "password": "password123",
        # Include other required fields here
    }
    response = client.post("/create/users", json=user_data)
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
    # Add more assertions based on your response model fields

def test_create_service():
    service_data = {
        "url": "https://example.com",
        # Include other required fields here
    }
    response = client.post("/create/services", json=service_data)
    assert response.status_code == 200
    assert response.json()["url"] == "https://example.com"
    # Add more assertions based on your response model fields

def test_create_role():
    role_data = {
        "name": "admin",
        # Include other required fields here
    }
    response = client.post("/create/roles", json=role_data)
    assert response.status_code == 200
    assert response.json()["name"] == "admin"
    # Add more assertions based on your response model fields

def test_create_permission():
    permission_data = {
        "name": "read",
        # Include other required fields here
    }
    response = client.post("/create/permissions", json=permission_data)
    assert response.status_code == 200
    assert response.json()["name"] == "read"
    # Add more assertions based on your response model fields

def test_create_role_permission():
    # Ensure you have valid role_id and permission_id values
    role_permission_data = {
        "role_id": 1,
        "permission_id": 1,
    }
    response = client.post("/create/role_permission", json=role_permission_data)
    assert response.status_code == 200
    # Add assertions based on your response model fields or any expected behavior

#endregion TEST: CREATE

#endregion TEST: CRUD ENDPOINTS