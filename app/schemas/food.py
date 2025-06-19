from pydantic import BaseModel
from typing import Optional, List
from .restaurant import RestaurantOut

class FoodSizeSchema(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        orm_mode = True


class FoodToppingSchema(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        orm_mode = True


class FoodOut(BaseModel):
    id: int
    name: str
    price: Optional[float]
    image: str
    description: Optional[str] = None
    restaurant: RestaurantOut
    sizes: List[FoodSizeSchema] = []
    toppings: List[FoodToppingSchema] = []

    class Config:
        orm_mode = True