from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from datetime import datetime, timedelta


class OrderItemCreate(BaseModel):
    cart_item_id: int


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    payment_method: str
    shipping_fee: Optional[int] = 0
    note: Optional[str] = ""
    address_id: int


class OrderStatus(str, Enum):
    pending = "Pending"
    to_pay = "To Pay"
    to_ship = "To Ship"
    to_receive = "To Receive"
    completed = "Completed"
    cancelled = "Cancelled"
    return_refund = "Return Refund"


STATUS_MAPPING = {
    "pending": OrderStatus.pending,
    "to pay": OrderStatus.to_pay,
    "to_pay": OrderStatus.to_pay,
    "to ship": OrderStatus.to_ship,
    "to_ship": OrderStatus.to_ship,
    "to receive": OrderStatus.to_receive,
    "to_receive": OrderStatus.to_receive,
    "completed": OrderStatus.completed,
    "cancelled": OrderStatus.cancelled,
    "can celled": OrderStatus.cancelled,
    "return refund": OrderStatus.return_refund,
    "return_refund": OrderStatus.return_refund
}


class OrderItemOut(BaseModel):
    foodName: str
    size: Optional[str]
    toppings: List[str]
    quantity: int
    price: float
    image: str


class OrderOut(BaseModel):
    orderID: str
    restaurant: str
    total: float
    createdAt: datetime
    status: OrderStatus
    items: List[OrderItemOut]
    note: Optional[str] = None
