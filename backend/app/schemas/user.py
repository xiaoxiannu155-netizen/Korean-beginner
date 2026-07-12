import uuid
from datetime import date
from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserRead(BaseModel):
    id: uuid.UUID
    email: str
    username: str | None
    avatar_url: str | None

    model_config = {"from_attributes": True}


class UserProgressRead(BaseModel):
    stage: int
    total_xp: int
    level: int
    streak_days: int
    last_active_date: date | None
    joy_name: str
    joy_gender: str
    joy_personality: str
    joy_display_mode: str

    model_config = {"from_attributes": True}


class RefreshRequest(BaseModel):
    refresh_token: str
