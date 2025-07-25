from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, func
from app.database.database import get_db
from app.model.food import Food
from app.model.restaurant import Restaurant
from app.schemas.food import FoodOut
from typing import List

search_router = APIRouter()

@search_router.get("/search", response_model=List[FoodOut])
def search_food(q: str, db: Session = Depends(get_db)):
    query_normalized = q.lower()

    results = (
        db.query(Food)
        .join(Food.restaurant)
        .options(
            joinedload(Food.restaurant),
            joinedload(Food.sizes),
            joinedload(Food.toppings),
        )
        .filter(
            or_(
                Food.name.ilike(f"%{q}%"),
                Restaurant.name.ilike(f"%{q}%"),
                func.unaccent(func.lower(Food.name)).ilike(f"%{query_normalized}%"),
                func.unaccent(func.lower(Restaurant.name)).ilike(f"%{query_normalized}%"),
            )
        )
        .all()
    )
    return results
