from sqlalchemy import Column, Integer, String, ForeignKey, Float
from app.database.database import Base
from sqlalchemy.orm import relationship

class Food(Base):
    __tablename__ = "food"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    image = Column(String, nullable=False)
    description = Column(String, nullable=False)
    
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    restaurant = relationship("Restaurant", back_populates="foods")
    sizes = relationship("FoodSize", back_populates="food")
    toppings = relationship("FoodTopping", back_populates="food")
    cart_items = relationship("CartItem", back_populates="food")



class FoodSize(Base):
    __tablename__= "food_sizes"

    id = Column(Integer, primary_key=True, index=True)
    food_id = Column(Integer, ForeignKey("food.id"))
    name = Column(String)
    price = Column(Float)

    food = relationship("Food", back_populates="sizes")



class FoodTopping(Base):
    __tablename__ = "food_toppings"
    id = Column(Integer, primary_key=True, index=True)
    food_id = Column(Integer, ForeignKey("food.id"))
    name = Column(String)
    price = Column(Float)

    food = relationship("Food", back_populates="toppings")
