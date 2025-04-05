from sqlalchemy import Column, Integer, String, ForeignKey
from app.db import Base

class Quiz(Base):
    _tablename_ = "quizzes"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    question = Column(String)
    answer = Column(String)

class Progress(Base):
    _tablename_ = "progress"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    completed = Column(Integer, default=0)