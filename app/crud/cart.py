from sqlalchemy.orm import Session
from app.model.cart import CartItem
from app.model.food import FoodTopping, FoodSize, Food
from app.schemas.cart import CartItemCreate
from fastapi import HTTPException


def toppings_match(existing_item: CartItem, new_topping_ids: list[int]) -> bool:
    existing_ids = sorted([t.id for t in existing_item.toppings])
    return existing_ids == sorted(new_topping_ids)


def create_cart_item(
    db: Session, user_id: int, item: CartItemCreate
) -> CartItem:
    # Kiểm tra món ăn có tồn tại
    food = db.query(Food).filter(Food.id == item.food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")

    # Kiểm tra size nếu có
    if item.selected_size_id:
        size = db.query(FoodSize).filter(FoodSize.id == item.selected_size_id).first()
        if not size:
            raise HTTPException(status_code=404, detail="Size not found")

    # Lấy danh sách topping nếu có
    topping_objs = []
    if item.topping_ids:
        topping_objs = db.query(FoodTopping).filter(FoodTopping.id.in_(item.topping_ids)).all()
        if len(topping_objs) != len(item.topping_ids):
            raise HTTPException(status_code=404, detail="One or more toppings not found")
    
    # Kiểm tra xem item này đã có trong giỏ hàng chưa
    existing_items = db.query(CartItem).filter(
        CartItem.user_id == user_id,
        CartItem.food_id == item.food_id,
        CartItem.selected_size_id == item.selected_size_id,
        CartItem.note == item.note  # Note cũng phải giống
    ).all()

    # So sánh topping
    for existing_item in existing_items:
        if toppings_match(existing_item, item.topping_ids or []):
            #  Nếu giống hệt → cộng dồn số lượng
            existing_item.quantity += item.quantity
            db.commit()
            db.refresh(existing_item)
            return existing_item

    #  Nếu chưa có → tạo mới cart item
    new_cart_item = CartItem(
        user_id=user_id,
        food_id=item.food_id,
        quantity=item.quantity,
        selected_size_id=item.selected_size_id,
        note=item.note
    )

    if topping_objs:
        new_cart_item.toppings = topping_objs

    db.add(new_cart_item)
    db.commit()
    db.refresh(new_cart_item)

    return new_cart_item

def get_cart_items(db: Session, user_id: int):
    return db.query(CartItem).filter(CartItem.user_id == user_id).all()


def update_cart_item_quantity(db: Session, user_id: int, cart_item_id: int, quantity: int):
    cart_item = db.query(CartItem).filter(
        CartItem.id == cart_item_id,
        CartItem.user_id == user_id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    if quantity <= 0:
        db.delete(cart_item)
    else:
        cart_item.quantity = quantity
        db.add(cart_item)

    db.commit()
    return cart_item


def delete_cart_item(db: Session, user_id: int, cart_item_id: int):
    cart_item = db.query(CartItem).filter(
        CartItem.id == cart_item_id,
        CartItem.user_id == user_id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()
    return True