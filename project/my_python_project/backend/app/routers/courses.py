from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.course import Course

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("/")
def list_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()

@router.get("/{course_id}")
def get_course(course_id: int, db: Session = Depends(get_db)):
    return db.query(Course).filter(Course.id == course_id).first()