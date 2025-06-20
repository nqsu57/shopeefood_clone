from pydantic import BaseModel
from typing import List, Optional

class CartItemCreate(BaseModel):
    food_id: int
    quantity: int
    selected_size_id: Optional[int] = None
    topping_ids: Optional[List[int]] = []
    note: Optional[str] = None