# Backend/app/tests/test_courses.py

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.schemas.course import CourseCreate, CourseUpdate
from backend.app.models import Course  # Import your Course model
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

# Test for creating a course
def test_create_course(client):
    course_data = {
        "title": "Test Course",
        "description": "This is a test course.",
        "price": 99.99,
        "instructor_id": 1,  # Assuming you have an instructor with ID 1 in your test DB
    }
    response = client.post("/courses/", json=course_data)
    assert response.status_code == 201  # Status code for created
    assert response.json()["title"] == course_data["title"]
    assert response.json()["price"] == course_data["price"]

# Test for getting a list of courses
def test_get_courses(client):
    response = client.get("/courses/")
    assert response.status_code == 200  # Status code for success
    assert isinstance(response.json(), list)  # Response should be a list

# Test for getting a single course by ID
def test_get_course_by_id(client):
    # Assuming a course with ID 1 exists
    response = client.get("/courses/1")
    assert response.status_code == 200  # Status code for success
    assert response.json()["id"] == 1
    assert "title" in response.json()

# Test for updating a course
def test_update_course(client):
    course_data = {
        "title": "Updated Course Title",
        "description": "This is an updated course description.",
        "price": 129.99,
    }
    response = client.put("/courses/1", json=course_data)  # Assuming course ID 1 exists
    assert response.status_code == 200  # Status code for success
    assert response.json()["title"] == course_data["title"]
    assert response.json()["price"] == course_data["price"]

# Test for deleting a course
def test_delete_course(client):
    # First, create a course to delete
    course_data = {
        "title": "Course to Delete",
        "description": "This course will be deleted.",
        "price": 59.99,
        "instructor_id": 1,
    }
    create_response = client.post("/courses/", json=course_data)
    course_id = create_response.json()["id"]
    
    # Now, delete the created course
    response = client.delete(f"/courses/{course_id}")
    assert response.status_code == 200  # Status code for success
    assert response.json()["id"] == course_id  # Ensure the correct course is deleted

# Test for getting a course that does not exist
def test_get_course_not_found(client):
    response = client.get("/courses/99999")  # Assuming this ID does not exist
    assert response.status_code == 404  # Not found
    assert response.json()["detail"] == "Course not found"