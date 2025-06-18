from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.schemas.user import AvatarUpdate
from app.database.database import get_db
from app.model.user import User
from sqlalchemy.orm import Session
avatar_update = APIRouter()

@avatar_update.put("/users/{user_id}/avatar")
def update_avatar(user_id: int, payload: AvatarUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.avatar_url = payload.avatar_url
    db.commit()
    return {"message": "Avatar updated", "avatar_url": user.avatar_url}