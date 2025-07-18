from sqlalchemy.orm import Session, joinedload
from app.model.cart import CartItem
from app.model.food import FoodTopping, FoodSize, Food
from app.schemas.cart import CartItemCreate
from fastapi import HTTPException
from app.model.restaurant import Restaurant


def toppings_match(existing_item: CartItem, new_topping_ids: list[int]) -> bool:
    existing_ids = sorted([t.id for t in existing_item.toppings])
    return existing_ids == sorted(new_topping_ids)


# def create_cart_item(
#     db: Session, user_id: int, item: CartItemCreate
# ) -> CartItem:
#     # Kiểm tra món ăn có tồn tại
#     food = db.query(Food).filter(Food.id == item.food_id).first()
#     if not food:
#         raise HTTPException(status_code=404, detail="Food not found")
    
    
#      # NEW: Kiểm tra & xử lý nhà hàng khác
#     existing_cart_items = db.query(CartItem).join(Food).filter(
#         CartItem.user_id == user_id
#     ).all()
#     existing_cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()


#     if existing_cart_items:
#         existing_restaurant_id = existing_cart_items[0].food.restaurant_id
#         new_restaurant_id = food.restaurant_id
        

#         if existing_restaurant_id != new_restaurant_id:
#             if not item.clear_cart:
#                 raise HTTPException(
#                     status_code=400,
#                     detail="Cart contains items from another restaurant. Set clear_cart=True to clear cart."
#                 )
#             else:
#                 # Xoá giỏ hàng
#                 for ci in existing_cart_items:
#                     db.delete(ci)
#                 db.commit()    

#     # Kiểm tra size nếu có
#     if item.selected_size_id:
#         size = db.query(FoodSize).filter(FoodSize.id == item.selected_size_id).first()
#         if not size:
#             raise HTTPException(status_code=404, detail="Size not found")

#     # Lấy danh sách topping nếu có
#     topping_objs = []
#     if item.topping_ids:
#         topping_objs = db.query(FoodTopping).filter(FoodTopping.id.in_(item.topping_ids)).all()
#         if len(topping_objs) != len(item.topping_ids):
#             raise HTTPException(status_code=404, detail="One or more toppings not found")
    
#     # Kiểm tra xem item này đã có trong giỏ hàng chưa
#     existing_items = db.query(CartItem).filter(
#         CartItem.user_id == user_id,
#         CartItem.food_id == item.food_id,
#         CartItem.selected_size_id == item.selected_size_id,
#         CartItem.note == item.note  # Note cũng phải giống
#     ).all()

#     # So sánh topping
#     for existing_item in existing_items:
#         if toppings_match(existing_item, item.topping_ids or []):
#             #  Nếu giống hệt → cộng dồn số lượng
#             existing_item.quantity += item.quantity
#             db.commit()
#             db.refresh(existing_item)
#             return existing_item

#     #  Nếu chưa có → tạo mới cart item
#     new_cart_item = CartItem(
#         user_id=user_id,
#         food_id=item.food_id,
#         quantity=item.quantity,
#         selected_size_id=item.selected_size_id,
#         note=item.note
#     )

#     if topping_objs:
#         new_cart_item.toppings = topping_objs

#     db.add(new_cart_item)
#     db.commit()
#     db.refresh(new_cart_item)

#     return new_cart_item

def create_cart_item(db: Session, user_id: int, item: CartItemCreate) -> CartItem:
    # Kiểm tra món ăn có tồn tại
    food = db.query(Food).filter(Food.id == item.food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Món ăn không tồn tại")
    
    # Lấy thông tin nhà hàng của món mới
    new_restaurant = db.query(Restaurant).filter(Restaurant.id == food.restaurant_id).first()
    if not new_restaurant:
        raise HTTPException(status_code=404, detail="Nhà hàng không tồn tại")
    
    # Kiểm tra giỏ hàng hiện tại của người dùng
    existing_cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()

    if existing_cart_items:
        # Kiểm tra nhà hàng của các món trong giỏ hàng
        existing_restaurant_id = None
        for ci in existing_cart_items:
            food_in_cart = db.query(Food).filter(Food.id == ci.food_id).first()
            if not food_in_cart:
                # Xóa món không hợp lệ khỏi giỏ hàng
                db.delete(ci)
                continue
            if existing_restaurant_id is None:
                existing_restaurant_id = food_in_cart.restaurant_id
            elif existing_restaurant_id != food_in_cart.restaurant_id:
                # Xóa toàn bộ giỏ hàng nếu phát hiện nhiều nhà hàng (ràng buộc 1 nhà hàng)
                db.query(CartItem).filter(CartItem.user_id == user_id).delete()
                db.commit()
                existing_cart_items = []
                break

        # Nếu giỏ hàng vẫn còn món, kiểm tra nhà hàng
        if existing_cart_items:
            existing_restaurant = db.query(Restaurant).filter(Restaurant.id == existing_restaurant_id).first()
            if existing_restaurant_id != food.restaurant_id:
                if not item.clear_cart:
                    # Trả về thông báo yêu cầu xác nhận xóa giỏ hàng
                    return {
                        "message": f"Giỏ hàng hiện chứa món từ nhà hàng '{existing_restaurant.name}'. Bạn có muốn xóa giỏ hàng để thêm món từ nhà hàng '{new_restaurant.name}'?",
                        "clear_cart_required": True,
                        "existing_restaurant": {"id": existing_restaurant.id, "name": existing_restaurant.name},
                        "new_restaurant": {"id": new_restaurant.id, "name": new_restaurant.name}
                    }
                else:
                    # Xóa giỏ hàng nếu clear_cart=True
                    db.query(CartItem).filter(CartItem.user_id == user_id).delete()
                    db.commit()

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
            # Nếu giống hệt → cộng dồn số lượng
            existing_item.quantity += item.quantity
            db.commit()
            db.refresh(existing_item)
            return existing_item

    # Nếu chưa có → tạo mới cart item
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


# def get_cart_items(db: Session, user_id: int):
#     return db.query(CartItem).filter(CartItem.user_id == user_id).all()

def get_cart_items(db: Session, user_id: int):
    return db.query(CartItem).options(
        joinedload(CartItem.food),
        joinedload(CartItem.selected_size),
        joinedload(CartItem.toppings)
    ).filter(CartItem.user_id == user_id).all()


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

def get_cart_summary(db: Session, user_id: int):
    cart_items = db.query(CartItem).options(
        joinedload(CartItem.food),
        joinedload(CartItem.selected_size),
        joinedload(CartItem.toppings)
    ).filter(CartItem.user_id == user_id).all()

    total_items = sum(item.quantity for item in cart_items)
    total_price = 0
    restaurant = None

    for item in cart_items:
        food_price = item.food.price or 0
        size_price = item.selected_size.price if item.selected_size else 0
        topping_price = sum(topping.price for topping in item.toppings)
        total_price += (food_price + size_price + topping_price) * item.quantity
        if item.food.restaurant_id and not restaurant:
            restaurant = db.query(Restaurant).filter(Restaurant.id == item.food.restaurant_id).first()

    return {
        "total_items": total_items,
        "total_price": total_price,
        "restaurant": {"id": restaurant.id, "name": restaurant.name} if restaurant else None,
        "items": cart_items
    }