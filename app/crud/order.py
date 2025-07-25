from sqlalchemy.orm import Session
from app.model.order import Order, OrderItem
from app.model.cart import CartItem
from app.schemas.order import OrderCreate

def create_order(db: Session, user_id: int, order_data: OrderCreate):
    # lấy cart items
    cart_items = db.query(CartItem).filter(
        CartItem.id.in_([i.cart_item_id for i in order_data.items]),
        CartItem.user_id == user_id
    ).all()

    if not cart_items:
        raise Exception("No valid cart items found")

    order = Order(
        user_id=user_id,
        restaurant_id=cart_items[0].food.restaurant_id,
        payment_method=order_data.payment_method,
        shipping_fee=order_data.shipping_fee or 0,
        address_id=order_data.address_id,
        note=order_data.note,
        total=0 
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    total_price = 0

    for cart_item in cart_items:
        base_price = cart_item.selected_size.price if cart_item.selected_size else cart_item.food.price
        topping_price = sum(topping.price for topping in cart_item.toppings)
        item_total = (base_price + topping_price) * cart_item.quantity
        total_price += item_total

        print('cart item food',cart_item.food)
        order_item = OrderItem(
            order_id=order.id,
            food_id=cart_item.food.id,
            food_name=cart_item.food.name,
            food_image=cart_item.food.image,
            quantity=cart_item.quantity,
            size_id=cart_item.selected_size.id if cart_item.selected_size else None,
            size_name=cart_item.selected_size.name if cart_item.selected_size else None,
            size_price=cart_item.selected_size.price if cart_item.selected_size else None,
            note=cart_item.note,
            item_total=item_total
        )

        order_item.toppings = list(cart_item.toppings)
        db.add(order_item)

    order.total = total_price + order.shipping_fee

    db.commit()

    # xoá cart
    for item in cart_items:
        db.delete(item)

    db.commit()

    return order
