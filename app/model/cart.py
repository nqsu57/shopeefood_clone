from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, Table, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.database import Base

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    food_id = Column(Integer, ForeignKey("food.id"))
    quantity = Column(Integer)
    selected_size_id = Column(Integer, ForeignKey("food_sizes.id"), nullable=True)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="cart_items")
    food = relationship("Food", back_populates="cart_items")
    selected_size = relationship("FoodSize")
    # toppings = relationship("CartItemTopping", back_populates="cart_item", cascade="all, delete-orphan")
    toppings = relationship("FoodTopping", secondary="cart_item_toppings", backref="cart_items")

# class CartItemTopping(Base):
#     __tablename__ = "cart_item_toppings"

#     cart_item_id = Column(Integer, ForeignKey("cart_items.id"), primary_key=True)
#     topping_id = Column(Integer, ForeignKey("food_toppings.id"), primary_key=True)

#     cart_item = relationship("CartItem", back_populates="toppings")
#     topping = relationship("FoodTopping")

cart_item_topping_table = Table(
    'cart_item_toppings',
    Base.metadata,
    Column('cart_item_id', Integer, ForeignKey('cart_items.id'), primary_key=True),
    Column('topping_id', Integer, ForeignKey('food_toppings.id'), primary_key=True)
)
