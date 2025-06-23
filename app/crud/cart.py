from sqlalchemy.orm import Session
from app.model import CartItem, CartItemTopping
from app.schemas.cart import CartItemCreate

def create_cart_item(db: Session, user_id: int, item: CartItemCreate):
    cart_item = CartItem(
        user_id=user_id,
        food_id=item.food_id,
        quantity=item.quantity,
        selected_size_id=item.selected_size_id,
        note=item.note,
    )
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    # Insert topping
    for topping_id in item.topping_ids:
        cart_item_topping = CartItemTopping(
            cart_item_id=cart_item.id,
            topping_id=topping_id,
        )
        db.add(cart_item_topping)

    db.commit()
    return cart_item


def get_cart_items(db: Session, user_id: int):
    return db.query(CartItem).filter(CartItem.user_id == user_id).all()
