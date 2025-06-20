from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.schemas.cart import CartItemCreate
from app.crud import cart as crud_cart
from app.core.security import get_db, get_current_user
from app.model.user import User

cart_router = APIRouter()

@cart_router.post("/cart/add")
def add_to_cart(item: CartItemCreate, 
                db: Session = Depends(get_db), 
                current_id: User = Depends(get_current_user)):
    
    return crud_cart.create_cart_item(db, user_id=current_id.id, item=item)
