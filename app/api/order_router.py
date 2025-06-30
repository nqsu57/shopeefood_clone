from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import get_db, get_current_user
from app.model.user import User
from app.schemas.order import OrderCreate
from app.crud import order as crud_order

order_router = APIRouter()

@order_router.post("/order")
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud_order.create_order(db, user_id=current_user.id, order_data=order)
