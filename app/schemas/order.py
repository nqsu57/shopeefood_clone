from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from datetime import datetime

class OrderItemCreate(BaseModel):
    cart_item_id: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    payment_method: str
    shipping_fee: Optional[int] = 0
    note: Optional[str] = ""
    address_id: int

class OrderStatus(str, Enum):
    to_pay = "To Pay"
    to_ship = "To Ship"
    to_receive = "To Receive"
    completed = "Completed"
    cancelled = "Cancelled"
    return_refund = "Return Refund"

class OrderOut(BaseModel):
    id: int
    restaurant: str
    foodName: str
    size: str
    toppings: List[str]
    quantity: int
    total: int
    createdAt: datetime
    status: OrderStatus
    image: str
