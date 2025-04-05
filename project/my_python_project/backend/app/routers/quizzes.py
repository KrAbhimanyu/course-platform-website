# Backend/app/routers/quizzes.py

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict

# Initialize the APIRouter instance
router = APIRouter()

# Pydantic models for request bodies
class Question(BaseModel):
    question_text: str
    options: List[str]
    correct_answer: int  # Index of the correct option (0-based)

class Quiz(BaseModel):
    title: str
    description: str
    questions: List[Question]

class Answer(BaseModel):
    question_id: int
    selected_answer: int  # The selected answer index (0-based)

class QuizSubmission(BaseModel):
    quiz_id: int
    answers: List[Answer]

# In-memory quiz data storage (use a database in production)
quizzes_db: Dict[int, Quiz] = {}
user_scores_db: Dict[int, Dict[int, int]] = {}  # user_scores_db[user_id][quiz_id] = score
quiz_counter = 0  # A simple counter for quiz IDs

# Endpoint to create a quiz
@router.post("/create_quiz", status_code=status.HTTP_201_CREATED)
async def create_quiz(quiz: Quiz):
    global quiz_counter
    quiz_id = quiz_counter
    quizzes_db[quiz_id] = quiz
    quiz_counter += 1
    return {"quiz_id": quiz_id, "message": "Quiz created successfully."}

# Endpoint to get a list of quizzes
@router.get("/get_quizzes", response_model=List[Quiz])
async def get_quizzes():
    return list(quizzes_db.values())

# Endpoint to get a specific quiz by ID
@router.get("/get_quiz/{quiz_id}", response_model=Quiz)
async def get_quiz(quiz_id: int):
    quiz = quizzes_db.get(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz

# Endpoint to submit a quiz and get a score
@router.post("/submit_quiz/{quiz_id}", status_code=status.HTTP_200_OK)
async def submit_quiz(quiz_id: int, submission: QuizSubmission):
    quiz = quizzes_db.get(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    # Check if the submitted answers are correct
    score = 0
    for answer in submission.answers:
        if answer.question_id < len(quiz.questions):
            correct_answer = quiz.questions[answer.question_id].correct_answer
            if answer.selected_answer == correct_answer:
                score += 1
    
    # Store the user's score for the quiz
    user_id = 1  # In real implementation, get the user ID from authentication
    if user_id not in user_scores_db:
        user_scores_db[user_id] = {}

    user_scores_db[user_id][quiz_id] = score

    return {"score": score, "message": "Quiz submitted successfully."}