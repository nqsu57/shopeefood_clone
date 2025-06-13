# routes/auth.py
# from fastapi import APIRouter, HTTPException, Depends
# from pydantic import EmailStr, BaseModel
# from jose import jwt, JWTError
# from datetime import datetime, timedelta
# from passlib.hash import bcrypt
# # from database.database import get_user_by_email, update_user_password 
# from app.services.email_services import send_reset_email_mailersend

# SECRET_KEY = "your-secret"
# ALGORITHM = "HS256"
# TOKEN_EXPIRE_MINUTES = 30

# forgot_password_router = APIRouter()
# reset_password_router = APIRouter()

# class EmailRequest(BaseModel):
#     email: EmailStr

# class ResetPasswordRequest(BaseModel):
#     token: str
#     new_password: str

# @forgot_password_router.post("/forgot-password")
# async def forgot_password(data: EmailRequest):
#     user = await get_user_by_email(data.email)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     print(user)
    
#     expires = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
#     token = jwt.encode({"sub": user.email, "exp": expires}, SECRET_KEY, algorithm=ALGORITHM)
    
#     await send_reset_email_mailersend(user.email, token)
#     return {"message": "Reset email sent"}

# @reset_password_router.post("/reset-password")
# async def reset_password(data: ResetPasswordRequest):
#     try:
#         payload = jwt.decode(data.token, SECRET_KEY, algorithms=[ALGORITHM])
#         email = payload.get("sub")
#         if email is None:
#             raise HTTPException(status_code=400, detail="Invalid token")
#     except JWTError:
#         raise HTTPException(status_code=400, detail="Invalid or expired token")
    
#     hashed = bcrypt.hash(data.new_password)
#     await update_user_password(email, hashed)
#     return {"message": "Password updated successfully"}
