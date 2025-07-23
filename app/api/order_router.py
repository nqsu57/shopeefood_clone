from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.core.security import get_db, get_current_user
from app.model.user import User
from app.schemas.order import OrderCreate, OrderOut, OrderItemOut, OrderStatus, STATUS_MAPPING
from app.crud import order as crud_order
from typing import Optional, List
from app.model.order import Order, OrderItem
from app.model.restaurant import Restaurant
from app.model.food import FoodTopping

order_router = APIRouter()

@order_router.get("/my-orders", response_model=List[OrderOut])
def get_orders(
    db: Session = Depends(get_db),
    status: Optional[str] = Query(None),
    current_user=Depends(get_current_user)
):
    query = db.query(Order).filter(Order.user_id == current_user.id)

    if status:
        query = query.filter(Order.status == status)

    orders = query.order_by(Order.created_at.desc()).all()
    result = []

    for order in orders:
        items_out = []
        for item in order.items:  # mối quan hệ one-to-many: order.items
            # bỏ qua nếu không có dữ liệu
            if not item.food_name:
                continue
            items_out.append(OrderItemOut(
                foodName=item.food_name or "",
                size=item.size_name,
                toppings=[t.name for t in item.toppings] if item.toppings else [],
                quantity=item.quantity or 0,
                price=item.item_total or 0.0, 
                image=item.food_image or ""
            ))

        result.append(OrderOut(
            orderID=str(order.orderID),
            restaurant=order.restaurant.name,
            createdAt=order.created_at,
            status=STATUS_MAPPING.get(order.status.lower(), OrderStatus.pending),
            total=order.total or 0.0,
            items=items_out,
            note=order.note
        ))

    return result


@order_router.post("/order", response_model=OrderOut)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_order = crud_order.create_order(db, user_id=current_user.id, order_data=order)

    order_items_out = []
    for item in db_order.items:
        toppings = [t.name for t in item.toppings]
        order_items_out.append(
            OrderItemOut(
            foodName=item.food_name or "",
            size=item.size_name,
            toppings=toppings,
            quantity=item.quantity,
            price=item.item_total,
            image=item.food_image or ""
        )
    )

    # ép status về Enum
    try:
        status_enum = OrderStatus(db_order.status)
    except ValueError:
        status_enum = OrderStatus.pending

    return OrderOut(
        orderID=db_order.orderID,
        restaurant=db_order.restaurant.name,
        total=db_order.total,
        createdAt=db_order.created_at,
        status=status_enum,
        items=order_items_out,
        note=db_order.note  
    )

@order_router.get("/orders/{orderID}")
def get_order_detail(
    orderID: str,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    order = (
        db.query(Order)
        .filter(Order.orderID == orderID)
        .first()
    )

    if not order:
        raise HTTPException(status_code=404, detail="Đơn hàng không tồn tại.")

    if user and order.user_id != user.id:
        raise HTTPException(status_code=403, detail="Bạn không có quyền xem đơn hàng này.")

    items_out = []
    for item in order.items:
        items_out.append({
            "foodName": item.food_name,
            "image": item.food_image,
            "size": item.size_name,
            "toppings": [t.name for t in item.toppings] if item.toppings else [],
            "quantity": item.quantity,
            "price": item.item_total
        })

    response = {
        "orderID": order.orderID,
        "restaurant": order.restaurant.name,
        "restaurantAddress": order.restaurant.address if hasattr(order.restaurant, "address") else None,
        "createdAt": order.created_at.isoformat(),
        "status": order.status,
        "total": order.total,
        "shippingFee": order.shipping_fee,
        "items": items_out
    }

    return response
