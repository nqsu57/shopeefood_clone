from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_db, pwd_context
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.model.user import User, UserRole, UserStatus
from app.crud.auth import normalize_phone

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    if db.query(User).filter(User.phone == user.phone).first():
        raise HTTPException(status_code=400, detail="Phone already registered")

    hashed_pw = pwd_context.hash(user.password)

    new_user = User(
        name=user.name, 
        phone=normalized_phone, 
        email=user.email, 
        hashed_password=hashed_pw, 
        role=UserRole.user, 
        status=UserStatus.active,
        is_verified=True)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user