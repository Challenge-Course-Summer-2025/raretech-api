from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    user_name: str
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class AdminInfoResponse(BaseModel):
    admin_id: str
    email: EmailStr
    user_name: str
    created_at: datetime
    updated_at: datetime
