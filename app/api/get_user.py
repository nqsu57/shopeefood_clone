from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user
from app.schemas.user import UserOut
from app.model.address import Address
from app.model.user import User
from sqlalchemy.orm import Session, joinedload
from app.database.database import get_db


get_user = APIRouter()

# @get_user.get("/get_user", response_model=UserOut)
# def get_user_info(current_user: User = Depends(get_current_user)):
#     return current_user

@get_user.get("/get_user", response_model=UserOut)
def get_user_info(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Load user kèm addresses & địa chỉ liên quan
    user = (
        db.query(User)
        .options(
            joinedload(User.addresses)
            .joinedload(Address.province),
            joinedload(User.addresses)
            .joinedload(Address.district),
            joinedload(User.addresses)
            .joinedload(Address.ward),
        )
        .filter(User.id == current_user.id)
        .first()
    )

    # lọc ra địa chỉ mặc định
#     default_address = next(
#     (addr for addr in user.addresses if getattr(addr, 'is_default', False)), None
# )
    default_address = (
        db.query(Address)
            .filter(Address.user_id == user.id, Address.is_default == True)
            .options(
                joinedload(Address.province),
                joinedload(Address.district),
                joinedload(Address.ward)
            )
            .first()
        )
    # trả về dict
    return {
        "id": user.id,
        "name": user.name,
        "phone": user.phone,
        "email": user.email,
        "gender": user.gender,
        "avatar_url": user.avatar_url,
        "default_address": default_address
    }