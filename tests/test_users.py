from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_get_user_profile():
    # Register and login
    email = "profileuser@example.com"
    client.post(
        "/api/auth/register",
        json={"email": email, "password": "Password123"}
    )
    login_resp = client.post(
        "/api/auth/login",
        json={"email": email, "password": "Password123"}
    )
    token = login_resp.json()["access_token"]

    # Get profile
    response = client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == email
    assert "password_hash" not in response.json()

def test_get_profile_unauthorized():
    response = client.get("/api/users/me")
    assert response.status_code == 401
