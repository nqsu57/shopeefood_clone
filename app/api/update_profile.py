from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import get_db, get_current_user
from app.model.user import User
from app.schemas import UserUpdate
from passlib.context import CryptContext

update_profile_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@update_profile_router.put("/users/update_profile")
def update_profile(
    update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated = False

    if update.name is not None:
        current_user.name = update.name
        updated = True

    if update.gender is not None:
        current_user.gender = update.gender
        updated = True

    if update.phone is not None:
        current_user.phone = update.phone
        updated = True

    if any([update.current_password, update.new_password, update.confirm_password]):
        if not update.current_password or not update.new_password or not update.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="All password fields must be provided."
            )

        if not pwd_context.verify(update.current_password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect."
            )

        if update.new_password != update.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New passwords do not match."
            )

        current_user.password = pwd_context.hash(update.new_password)
        updated = True

    if updated:
        db.commit()
        db.refresh(current_user)
        return {"message": "Profile updated successfully"}

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="No changes provided."
    )
