from fastapi import APIRouter, Depends,  HTTPException, Path
from typing import List
from app.schemas.food import FoodOut as FoodOut
from app.model.food import Food as FoodModel
from app.database.database import get_db
from sqlalchemy.orm import Session



foods = APIRouter()
detail_food = APIRouter()

@foods.get("/foods", response_model=List[FoodOut])
def get_foods(db: Session = Depends(get_db)):
    return db.query(FoodModel).all()

@detail_food.get("/food/{food_id}", response_model=FoodOut)
def get_food_by_id(food_id: int = Path(..., gt=0), db: Session = Depends(get_db)): 
    food = db.query(FoodModel).filter(FoodModel.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    if food.sizes:
        food.price = None
    return food