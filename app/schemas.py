from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    name: str
    phone: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    phone: str
    name: str
    email: EmailStr

    class Config:
        orm_mode = True

class UserOut(BaseModel):
    id: int
    name: str
    phone: str
    email: EmailStr
    gender: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    current_password: Optional[str] = None
    new_password: Optional[str] = None
    confirm_password: Optional[str] = None

class AvatarUpdate(BaseModel):
    avatar_url: str