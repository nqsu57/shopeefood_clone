from pydantic import BaseModel
from typing import Optional
from .restaurant import RestaurantOut


class FoodOut(BaseModel):
    id: int
    name: str
    price: int
    image: str
    description: Optional[str] = None
    restaurant: RestaurantOut

    class Config:
        orm_mode = True