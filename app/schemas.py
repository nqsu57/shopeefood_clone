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

class UserOut(BaseModel):
    # full_name: str
    phone: str
    email: EmailStr

class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str
