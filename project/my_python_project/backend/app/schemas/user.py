# Backend/app/schemas/user.py

from pydantic import BaseModel, EmailStr
from typing import Optional

# Pydantic model for user registration
class UserCreate(BaseModel):
    username: str  # The username chosen by the user
    email: EmailStr  # The email address of the user
    password: str  # The password chosen by the user

    class Config:
        orm_mode = True  # Allows ORM models to be converted into Pydantic models

# Pydantic model for user login (usually used for token generation)
class UserLogin(BaseModel):
    username: str  # The username of the user
    password: str  # The password of the user

# Pydantic model for a user's profile (response)
class UserProfile(BaseModel):
    id: int  # User ID
    username: str  # The username of the user
    email: EmailStr  # The email address of the user
    created_at: str  # Timestamp of account creation

    class Config:
        orm_mode = True  # Allows ORM models to be converted into Pydantic models

# Pydantic model for updating user profile information
class UserUpdate(BaseModel):
    username: Optional[str]  # Username to update (optional)
    email: Optional[EmailStr]  # Email to update (optional)
    password: Optional[str]  # Password to update (optional)

# Pydantic model for user password reset request
class UserPasswordResetRequest(BaseModel):
    email: EmailStr  # Email of the user requesting password reset

# Pydantic model for resetting the password
class UserPasswordReset(BaseModel):
    token: str  # The reset token received via email
    new_password: str  # The new password for the user