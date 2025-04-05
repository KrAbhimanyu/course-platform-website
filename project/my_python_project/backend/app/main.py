
# Backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import users, courses, quizzes, upload, auth, seed
from .db import init_db  # Optional: Initialize the database if needed

# Initialize the FastAPI app with metadata
app = FastAPI(
    title="Course Platform API",
    description="API for managing courses, users, quizzes, uploads, and more.",
    version="1.0.0",
)

# Adding CORS middleware to allow cross-origin requests (useful for frontend development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific domains for production security
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Allow all headers
)

# Include routers for different parts of the app
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(courses.router, prefix="/courses", tags=["Courses"])
app.include_router(quizzes.router, prefix="/quizzes", tags=["Quizzes"])
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(seed.router, prefix="/seed", tags=["Seed"])

# Optional: Database initialization on app startup (if using a database)
@app.on_event("startup")
async def startup():
    # Initialize the database here, if necessary (e.g., SQLite, PostgreSQL, etc.)
    init_db()

# Simple health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "Healthy"}

# Main entry point when the app runs
if __name__ == "_main_":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)










# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.routers import auth, courses, quizzes, upload, payments
# from app.db import Base, engine

# Base.metadata.create_all(bind=engine)

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

# app.include_router(auth.router)
# app.include_router(courses.router)
# app.include_router(quizzes.router)
# app.include_router(upload.router)
# app.include_router(payments.router)