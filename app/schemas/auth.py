from pydantic import BaseModel, EmailStr, Field

class RequestOTP(BaseModel):
    phone: str

class VerifyOTP(BaseModel):
    phone: str
    otp: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str = Field(..., description="Reset token từ email")
    new_password: str

class EmailRequest(BaseModel):
    email: str
