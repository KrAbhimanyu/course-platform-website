# Backend/app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

# Models (for request bodies)
class User(BaseModel):
    username: str
    password: str

class UserInDB(User):
    hashed_password: str

# FastAPI router instance
router = APIRouter()

# Dependency to get the current user
def get_user_from_db(username: str):
    # Replace this with actual database query to get the user
    fake_user_db = {
        "testuser": {
            "username": "testuser",
            "hashed_password": "$2b$12$ZPEnZCmCjPyqHyj5RAfBTeTdeX3H5v5VpdQzI6k1/hY1gzXck1iZe",  # hashed 'password'
        }
    }
    return fake_user_db.get(username)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = "7a0e0848f8298c2c0a3b8f256f7174239a6fdbd9d76265d0b760019ff351f5ff"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Function to hash passwords
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Function to verify passwords
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Function to create JWT access token
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# User registration endpoint
@router.post("/register")
async def register(user: User):
    """Register a new user."""
    fake_user_db = {
        "testuser": {
            "username": "testuser",
            "hashed_password": "$2b$12$ZPEnZCmCjPyqHyj5RAfBTeTdeX3H5v5VpdQzI6k1/hY1gzXck1iZe",  # Example hashed password
        }
    }

    if user.username in fake_user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    
    hashed_password = hash_password(user.password)
    fake_user_db[user.username] = {"username": user.username, "hashed_password": hashed_password}
    return {"message": "User registered successfully!"}

# User login endpoint
@router.post("/login")
async def login(user: User):
    """Login and return a JWT token."""
    db_user = get_user_from_db(user.username)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    
    if not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Function to get the current user from JWT token
async def get_current_user(token: str = Depends(...)):
    """Get current user based on token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception