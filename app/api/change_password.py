from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.model.user import User  # Model ORM
from app.database.database import get_db
from app.core.security import get_current_user, verify_password, hash_password
from app.schemas import PasswordChangeRequest
change_password_user = APIRouter()

@change_password_user.put("/users/change_password_user")
def change_password(
    data: PasswordChangeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not verify_password(data.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Mật khẩu hiện tại không đúng")

    if data.new_password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Mật khẩu mới không khớp")

    current_user.hashed_password = hash_password(data.new_password)
    db.commit()

    return {"message": "Cập nhật mật khẩu thành công"}
