from fastapi import APIRouter, Depends, Request, status, HTTPException
from typing import List
from sqlalchemy.orm import Session, joinedload
from app.schemas.cart import CartItemCreate, CartItemOut, UpdateQuantity
from app.crud import cart as crud_cart
from app.core.security import get_db, get_current_user
from app.model.user import User
from app.model.cart import CartItem

cart_router = APIRouter()

@cart_router.post("/cart/add")
def add_to_cart(item: CartItemCreate, 
                db: Session = Depends(get_db), 
                current_id: User = Depends(get_current_user)):
    return crud_cart.create_cart_item(db, user_id=current_id.id, item=item)

@cart_router.get("/cart", response_model=List[CartItemOut])
def get_my_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    # return crud_cart.get_cart_items(db, user_id= current_user.id)
    # cart_items = db.query(CartItem).filter(CartItem.user_id == current_user.id).all()
    cart_items = db.query(CartItem).options(
        joinedload(CartItem.food),
        joinedload(CartItem.selected_size),
        joinedload(CartItem.toppings)
    ).filter(CartItem.user_id == current_user.id).all()
    return cart_items


@cart_router.patch("/cart/{cart_item_id}")
def update_quantity(
    cart_item_id: int,
    update: UpdateQuantity,  
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart_item = db.query(CartItem).filter(
        CartItem.id == cart_item_id,
        CartItem.user_id == current_user.id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    cart_item.quantity = update.quantity
    db.commit()
    db.refresh(cart_item)

    return {"detail": "Quantity updated", "quantity": cart_item.quantity}

@cart_router.delete("/cart/{cart_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cart_item(
    cart_item_id: int,
    db: Session = Depends(get_db),
     current_user: User = Depends(get_current_user)
):
    crud_cart.delete_cart_item(
        db, user_id=current_user.id, cart_item_id=cart_item_id
    )
    return {"detail": "Cart item deleted"}