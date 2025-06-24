from pydantic import BaseModel, Field
from typing import List, Optional

class CartItemCreate(BaseModel):
    food_id: int
    quantity: int
    selected_size_id: Optional[int] = None
    topping_ids: Optional[List[int]] = []
    note: Optional[str] = None

class FoodInfo(BaseModel):
    id: int
    name: str
    image: Optional[str]
    price: Optional[int]

    class Config:
        orm_mode = True

class SizeInfo(BaseModel):
    id: int
    name: str
    price: int

    class Config:
        orm_mode = True

class ToppingInfo(BaseModel):
    id: int
    name: str
    price: int

    class Config:
        orm_mode = True

class CartItemOut(BaseModel):
    id: int
    quantity: int
    note: Optional[str]
    # created_at: datetime

    food: FoodInfo
    selected_size: Optional[SizeInfo]
    # toppings: List[ToppingInfo] = []
    toppings: List[ToppingInfo] = Field(..., alias="toppings_list")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True 