from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.model.user import User
from app.core.security import verify_password, create_access_token

login_router = APIRouter()

@login_router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password!")
    
    if user.is_verified is False:
        raise HTTPException(status_code=403, detail="Account is not verified or has been disabled.")
    
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
