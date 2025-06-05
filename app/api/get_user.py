from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.schemas import UserOut
from app.model.user import User

get_user = APIRouter()

@get_user.get("/get_user", response_model=UserOut)
def get_user_info(current_user: UserOut = Depends(get_current_user)):
    return current_user

# @get_user.get("/get_user", response_model=UserOut)
# def get_user(current_user: User = Depends(get_current_user)):
#         return {"user": "data"}
