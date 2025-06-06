from pydantic import BaseModel, EmailStr

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
    name: str
    phone: str
    email: EmailStr

class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str
