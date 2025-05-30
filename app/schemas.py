from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    phone: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    phone: str
    email: EmailStr

    class Config:
        orm_mode = True