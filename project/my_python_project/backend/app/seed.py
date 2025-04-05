# Backend/app/routers/seed.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from random import randint

# Initialize the APIRouter instance
router = APIRouter()

# Pydantic models for request bodies (same as your course, quiz, or user models)
class User(BaseModel):
    username: str
    email: str
    hashed_password: str

class Course(BaseModel):
    title: str
    description: str
    instructor: str

class Question(BaseModel):
    question_text: str
    options: list
    correct_answer: int

class Quiz(BaseModel):
    title: str
    description: str
    questions: list


# Mock data storage (use a real database in production)
users_db = {}
courses_db = {}
quizzes_db = {}

# Seeding users into the database
def seed_users():
    users_db["admin"] = User(username="admin", email="admin@example.com", hashed_password="hashedpassword")
    users_db["testuser"] = User(username="testuser", email="testuser@example.com", hashed_password="hashedpassword")
    print("Seeded Users")

# Seeding courses into the database
def seed_courses():
    courses_db[1] = Course(
        title="Python Programming for Beginners",
        description="Learn the basics of Python programming",
        instructor="John Doe"
    )
    courses_db[2] = Course(
        title="Advanced JavaScript",
        description="Deep dive into JavaScript and modern frameworks",
        instructor="Jane Smith"
    )
    print("Seeded Courses")

# Seeding quizzes into the database
def seed_quizzes():
    quiz_1 = Quiz(
        title="Python Basics Quiz",
        description="Test your knowledge of basic Python programming",
        questions=[
            Question(question_text="What is 2 + 2?", options=["3", "4", "5"], correct_answer=1),
            Question(question_text="What does 'print' do in Python?", options=["Prints text", "Adds two numbers", "Divides numbers"], correct_answer=0)
        ]
    )
    quiz_2 = Quiz(
        title="JavaScript Basics Quiz",
        description="Test your knowledge of basic JavaScript programming",
        questions=[
            Question(question_text="Which symbol is used for comments in JavaScript?", options=["//", "/*", "#"], correct_answer=0),
            Question(question_text="What is the result of 10 + '10' in JavaScript?", options=["'1010'", "20", "NaN"], correct_answer=0)
        ]
    )
    quizzes_db[1] = quiz_1
    quizzes_db[2] = quiz_2
    print("Seeded Quizzes")

# Seed all data
@router.post("/seed_all", status_code=200)
async def seed_all():
    """Seed users, courses, and quizzes into the database."""
    try:
        seed_users()
        seed_courses()
        seed_quizzes()
        return {"message": "Seeding completed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Optional: Add more seeding functions for other models (like enrollments, progress tracking, etc.)