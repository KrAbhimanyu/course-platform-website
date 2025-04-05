# Backend/app/tests/test_auth.py

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.schemas.user import UserCreate
from backend.app.models import User  # Import your User model
from backend.app.db import init_db, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create a testing database session
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Use an in-memory SQLite database for testing
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency override to use the test database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override the dependency for testing
app.dependency_overrides[get_db] = override_get_db

# Initialize the app and database for testing
@pytest.fixture(scope="module")
def client():
    # Initialize the database (create tables)
    init_db()
    
    # Set up the test client
    with TestClient(app) as client:
        yield client

# Test for user registration
def test_register(client):
    user_data = {
        "email": "testuser@example.com",
        "password": "testpassword123",
        "username": "testuser",
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201  # Status code for created
    assert response.json()["email"] == user_data["email"]
    assert "access_token" in response.json()

# Test for user login
def test_login(client):
    login_data = {
        "username": "testuser",
        "password": "testpassword123",
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200  # Status code for success
    assert "access_token" in response.json()

# Test for invalid login (wrong password)
def test_login_invalid_password(client):
    login_data = {
        "username": "testuser",
        "password": "wrongpassword",
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 401  # Unauthorized
    assert response.json()["detail"] == "Invalid credentials"

# Test for unauthorized access to protected routes
def test_protected_route(client):
    # First, get the token by logging in
    login_data = {
        "username": "testuser",
        "password": "testpassword123",
    }
    response = client.post("/auth/login", data=login_data)
    token = response.json()["access_token"]
    
    # Now, try accessing a protected route
    response = client.get(
        "/protected_route",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200  # Protected route should be accessible with a valid token

# Test for accessing protected route without token (unauthorized)
def test_protected_route_without_token(client):
    response = client.get("/protected_route")
    assert response.status_code == 401  # Unauthorized, no token provided
    assert response.json()["detail"] == "Not authenticated"