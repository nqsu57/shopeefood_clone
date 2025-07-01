from sqlalchemy.orm import Session
from app.model.order import Order, OrderItem
from app.model.cart import CartItem
from app.schemas.order import OrderCreate

def create_order(db: Session, user_id: int, order_data: OrderCreate):
    cart_items = db.query(CartItem).filter(
        CartItem.id.in_([i.cart_item_id for i in order_data.items]),
        CartItem.user_id == user_id
    ).all()

    if not cart_items:
        raise Exception("No valid cart items found")

    total_price = 0
    for item in cart_items:
        base_price = item.selected_size.price if item.selected_size else item.food.price
        topping_total = sum([topping.price for topping in item.toppings])        
        total_price += (base_price + topping_total) * item.quantity

    total_price += order_data.shipping_fee or 0

    order = Order(
        user_id=user_id,
        payment_method=order_data.payment_method,
        shipping_fee=order_data.shipping_fee or 0,
        total=total_price,
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    # for cart_item in cart_items:
    #     order_item = OrderItem(order_id=order.id, cart_item_id=cart_item.id)
    #     db.add(order_item)
    for item in cart_items:
        base_price = item.selected_size.price if item.selected_size else item.food.price
        topping_price = sum([topping.price for topping in item.toppings])
        item_total = (base_price + topping_price) * item.quantity
        total_price += item_total

        order_item = OrderItem(
            order_id=order.id,
            food_id=item.food.id,
            food_name=item.food.name,
            food_image=item.food.image,
            quantity=item.quantity,
            size_id=item.selected_size.id if item.selected_size else None,
            size_name=item.selected_size.name if item.selected_size else None,
            size_price=item.selected_size.price if item.selected_size else None,
            note=item.note
        )
        order_item.toppings = item.toppings.copy()
        db.add(order_item)

    order.total = total_price + order.shipping_fee
    db.commit()
    for item in cart_items:
        db.delete(item)
    db.commit()
    return order
