from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.security import get_db, get_current_user
from app.model.user import User
from app.schemas.order import OrderCreate, OrderOut
from app.crud import order as crud_order
from typing import Optional, List
from app.model.order import Order


order_router = APIRouter()

@order_router.get("/orders", response_model=List[OrderOut])
def get_orders(db: Session = Depends(get_db), status: Optional[str] = Query(None, description="Trạng thái đơn hàng"), current_user=Depends(get_current_user)):
    query = db.query(Order).filter(Order.user_id == current_user.id)

    if status:
        query = query.filter(Order.status == status)

    return query.all()

@order_router.post("/order")
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud_order.create_order(db, user_id=current_user.id, order_data=order)
