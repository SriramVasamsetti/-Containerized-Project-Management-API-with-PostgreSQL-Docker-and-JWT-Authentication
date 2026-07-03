import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database.database import Base, engine

client = TestClient(app)

def test_register_user():
    # Clean database state for test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post(
        "/api/auth/register",
        json={"email": "newuser@example.com", "password": "Password123"}
    )
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["email"] == "newuser@example.com"

def test_register_duplicate_email():
    client.post(
        "/api/auth/register",
        json={"email": "duplicate@example.com", "password": "Password123"}
    )
    response = client.post(
        "/api/auth/register",
        json={"email": "duplicate@example.com", "password": "Password123"}
    )
    assert response.status_code == 409

def test_login_success():
    client.post(
        "/api/auth/register",
        json={"email": "loginuser@example.com", "password": "Password123"}
    )
    response = client.post(
        "/api/auth/login",
        json={"email": "loginuser@example.com", "password": "Password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_invalid_credentials():
    response = client.post(
        "/api/auth/login",
        json={"email": "loginuser@example.com", "password": "WrongPassword"}
    )
    assert response.status_code == 401
