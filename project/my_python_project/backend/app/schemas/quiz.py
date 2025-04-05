# Backend/app/schemas/quiz.py

from pydantic import BaseModel
from typing import List, Optional

# Pydantic model for a question in a quiz
class QuestionBase(BaseModel):
    question_text: str  # The question text
    options: List[str]  # List of possible answers
    correct_answer: int  # The index of the correct answer in the options list (0-based)

# Pydantic model for creating a new quiz
class QuizCreate(BaseModel):
    title: str  # Title of the quiz
    description: str  # Description of the quiz
    questions: List[QuestionBase]  # List of questions in the quiz

# Pydantic model for the response when retrieving quiz data
class QuizResponse(QuizCreate):
    id: int  # ID of the quiz in the database

    class Config:
        orm_mode = True  # Allows ORM models to be converted into Pydantic models

# Pydantic model for submitting answers to a quiz
class Answer(BaseModel):
    question_id: int  # ID of the question being answered
    selected_answer: int  # The selected answer index (0-based)

# Pydantic model for quiz submission, including answers
class QuizSubmission(BaseModel):
    quiz_id: int  # ID of the quiz being submitted
    answers: List[Answer]  # List of answers submitted by the user

# Pydantic model for the score of a quiz submission
class QuizScore(BaseModel):
    quiz_id: int  # ID of the quiz
    user_id: int  # ID of the user who took the quiz
    score: int  # The score the user achieved on the quiz