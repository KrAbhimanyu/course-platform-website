# Backend/app/schemas/course.py

from pydantic import BaseModel
from typing import List, Optional

# Pydantic model for course content (e.g., lessons, videos)
class CourseContentBase(BaseModel):
    title: str  # The title of the lesson or content
    description: str  # Description of the lesson or content
    content_type: str  # Type of content (e.g., video, article, PDF)

# Pydantic model for creating a new course
class CourseCreate(BaseModel):
    title: str  # Title of the course
    description: str  # Description of the course
    content: List[CourseContentBase]  # List of content included in the course

# Pydantic model for the response when retrieving course data
class CourseResponse(CourseCreate):
    id: int  # ID of the course in the database
    created_at: str  # Timestamp when the course was created
    updated_at: str  # Timestamp when the course was last updated

    class Config:
        orm_mode = True  # Allows ORM models to be converted into Pydantic models

# Pydantic model for updating a course
class CourseUpdate(BaseModel):
    title: Optional[str]  # Title of the course (optional for update)
    description: Optional[str]  # Description of the course (optional for update)
    content: Optional[List[CourseContentBase]]  # List of content (optional for update)

# Pydantic model for student enrollment in a course
class Enrollment(BaseModel):
    course_id: int  # ID of the course to enroll in
    student_id: int  # ID of the student enrolling in the course

# Pydantic model for retrieving student enrollment details
class EnrollmentResponse(Enrollment):
    id: int  # Enrollment ID
    status: str  # Enrollment status (e.g., enrolled, completed)

# Pydantic model for the student's progress in a course
class CourseProgress(BaseModel):
    course_id: int  # ID of the course
    student_id: int  # ID of the student
    progress: float  # Progress percentage (0-100%)

# Pydantic model for course ratings and reviews
class CourseReview(BaseModel):
    course_id: int  # ID of the course being reviewed
    student_id: int  # ID of the student reviewing the course
    rating: int  # Rating out of 5
    review_text: Optional[str]  # Optional review text