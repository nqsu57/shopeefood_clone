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
        topping_price = sum([t.topping.price for t in item.toppings])
        total_price += (base_price + topping_price) * item.quantity

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

    for cart_item in cart_items:
        order_item = OrderItem(order_id=order.id, cart_item_id=cart_item.id)
        db.add(order_item)

    db.commit()
    return order
