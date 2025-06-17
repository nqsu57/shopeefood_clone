from fastapi import APIRouter, Depends,  HTTPException, Path
from typing import List
from app.schemas import Food as FoodSchema
from app.model.food import Food as FoodModel
from app.database.database import get_db
from sqlalchemy.orm import Session



foods = APIRouter()
detail_food = APIRouter()

@foods.get("/foods", response_model=List[FoodSchema])
def get_foods(db: Session = Depends(get_db)):
    # return [
    #     Food(id=1,name="Bún bò Huế",price=40000,image="https://down-tx-vn.img.susercontent.com/vn-11134513-7r98o-lsu0q1909dj890@resize_ss640x400!@crop_w640_h400_cT"),
    #     Food(id=2,name="Cơm tấm",price=35000,image="https://down-tx-vn.img.susercontent.com/vn-11134513-7r98o-lsveduq715eh66@resize_ss640x400!@crop_w640_h400_cT"),
    #     Food(id=3,name="Phở bò",price=45000,image="https://down-tx-vn.img.susercontent.com/vn-11134513-7r98o-lxg9s7jbepy325@resize_ss640x400!@crop_w640_h400_cT"),
    #     Food(id=4,name="Bánh canh cua",price=55000,image="https://down-tx-vn.img.susercontent.com/vn-11134513-7r98o-lsv8tidvf6bo6f@resize_ss640x400!@crop_w640_h400_cT")
    # ]
    return db.query(FoodModel).all()

@detail_food.get("/food/{food_id}", response_model=FoodSchema)
def get_food_by_id(food_id: int = Path(..., gt=0), db: Session = Depends(get_db)): 
    food = db.query(FoodModel).filter(FoodModel.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    return food