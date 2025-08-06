from fastapi import HTTPException, APIRouter, Depends
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.schemas.auth import ForgotPasswordRequest, ResetPasswordRequest, EmailRequest
from app.model.user import User
from app.database.database import get_db
from app.core.security import SECRET_KEY, ALGORITHM, pwd_context
from sqlalchemy.orm import Session
from app.core.security import create_reset_token
from app.services.email_services import send_reset_password_email
from app.utils.mail import send_reset_password_email_test


auth_mail_router = APIRouter()

@auth_mail_router.post("/auth/forgot-password")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if user:
        token = create_reset_token(data={"sub": user.email})
        reset_url = f"http://localhost:5173/reset-password?token={token}"
        send_reset_password_email(to_email=user.email, reset_link=reset_url)

    # Luôn trả về thông báo chung
    return {"message": "Chúng tôi đã gửi hướng dẫn đặt lại mật khẩu"}


@auth_mail_router.post("/auth/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(request.token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="The token is invalid.")
    except JWTError:
        raise HTTPException(status_code=400, detail="The token is invalid or has expired.")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="The user does not exist.")

    # Hash mật khẩu mới
    user.hashed_password = pwd_context.hash(request.new_password)
    db.commit()

    return {"message": "The password has been successfully reset."}


# Test Mail
@auth_mail_router.post("/forgot-password-test")
def forgot_password_test(request: EmailRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="The email is not registered")

    token = create_reset_token(data={"sub": user.email})
    reset_link = f"http://localhost:5173/reset-password?token={token}"

    try:
        send_reset_password_email_test(request.email, reset_link)
        return {"message": "The email has been sent."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {e}")