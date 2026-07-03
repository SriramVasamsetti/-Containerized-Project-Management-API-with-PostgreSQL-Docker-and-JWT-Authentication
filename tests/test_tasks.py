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

def test_task_crud_and_cascade():
    headers = get_auth_headers("taskowner@example.com")

    # Create Project
    proj_resp = client.post(
        "/api/projects",
        json={"name": "Task Project"},
        headers=headers
    )
    project_id = proj_resp.json()["id"]

    # Create Task
    task_resp = client.post(
        f"/api/projects/{project_id}/tasks",
        json={"title": "Task 1", "status": "TODO"},
        headers=headers
    )
    assert task_resp.status_code == 201
    task_id = task_resp.json()["id"]

    # Get Task
    get_resp = client.get(f"/api/tasks/{task_id}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "Task 1"

    # Update Task
    update_resp = client.put(
        f"/api/tasks/{task_id}",
        json={"status": "IN_PROGRESS"},
        headers=headers
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "IN_PROGRESS"

    # Delete Project (Triggers Cascade Delete)
    del_proj_resp = client.delete(f"/api/projects/{project_id}", headers=headers)
    assert del_proj_resp.status_code == 204

    # Verify Task is deleted
    get_task_resp = client.get(f"/api/tasks/{task_id}", headers=headers)
    assert get_task_resp.status_code == 404
