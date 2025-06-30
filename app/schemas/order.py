from pydantic import BaseModel
from typing import List, Optional

class OrderItemCreate(BaseModel):
    cart_item_id: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    payment_method: str
    shipping_fee: Optional[int] = 0
    note: Optional[str] = ""