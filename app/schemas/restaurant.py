from pydantic import BaseModel
# from typing import Optional

class RestaurantOut(BaseModel):
    id: int
    name: str
    address: str

    class Config:
        orm_mode = True