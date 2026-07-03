from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def get_auth_headers(email: str):
    client.post(
        "/api/auth/register",
        json={"email": email, "password": "Password123"}
    )
    login_resp = client.post(
        "/api/auth/login",
        json={"email": email, "password": "Password123"}
    )
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_project_crud():
    headers = get_auth_headers("projectowner@example.com")

    # Create Project
    create_resp = client.post(
        "/api/projects",
        json={"name": "New Project", "description": "Project Description"},
        headers=headers
    )
    assert create_resp.status_code == 201
    project_id = create_resp.json()["id"]

    # Get Project
    get_resp = client.get(f"/api/projects/{project_id}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "New Project"

    # Update Project
    update_resp = client.put(
        f"/api/projects/{project_id}",
        json={"name": "Updated Project Name"},
        headers=headers
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == "Updated Project Name"

    # Delete Project
    delete_resp = client.delete(f"/api/projects/{project_id}", headers=headers)
    assert delete_resp.status_code == 204

def test_project_ownership_enforcement():
    owner_headers = get_auth_headers("owner@example.com")
    stranger_headers = get_auth_headers("stranger@example.com")

    # Owner creates project
    create_resp = client.post(
        "/api/projects",
        json={"name": "Secret Project"},
        headers=owner_headers
    )
    project_id = create_resp.json()["id"]

    # Stranger tries to access
    get_resp = client.get(f"/api/projects/{project_id}", headers=stranger_headers)
    assert get_resp.status_code == 403

    # Stranger tries to update
    update_resp = client.put(
        f"/api/projects/{project_id}",
        json={"name": "Hacked Name"},
        headers=stranger_headers
    )
    assert update_resp.status_code == 403

    # Stranger tries to delete
    delete_resp = client.delete(f"/api/projects/{project_id}", headers=stranger_headers)
    assert delete_resp.status_code == 403
