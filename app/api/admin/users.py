from fastapi import APIRouter, Depends, HTTPException
from app.core.security import admin_required
from app.schemas.user import UserOut
from app.model.address import Address
from app.model.user import User
from sqlalchemy.orm import Session, joinedload
from app.database.database import get_db
from typing import Optional, List
from sqlalchemy import or_

admin_user_router  = APIRouter()

@admin_user_router.get("/admin/users", response_model=List[UserOut])
def get_users(
    role: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    # limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    if search:
        query = query.filter(or_(User.email.ilike(f"%{search}%"), User.phone.ilike(f"%{search}%")))
    users = query.offset(skip).all()
    return users


@admin_user_router.get("/admin/users/{user_id}", response_model=UserOut)
def get_user_detail(user_id: int, db: Session = Depends(get_db), current_user=Depends(admin_required)):
    user = db.query(User).options(
        joinedload(User.driver_profile),
        joinedload(User.restaurant_profile),
        joinedload(User.addresses),
    ).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user