import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Table
from sqlalchemy.orm import relationship
from app.database.database import Base
from sqlalchemy.sql import func


def generate_order_id():
    return str(uuid.uuid4()).replace("-", "").upper()[:12]


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    orderID = Column(String(20), unique=True, index=True, nullable=False, default=generate_order_id)    
    payment_method = Column(String, default="COD")
    shipping_fee = Column(Integer, default=0)
    total = Column(Float, default=0)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    address_id = Column(Integer, ForeignKey("addresses.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)


    user = relationship("User")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete")
    address = relationship("Address", back_populates="orders")
    restaurant = relationship("Restaurant")

order_item_topping_table = Table(
    'order_item_toppings',
    Base.metadata,
    Column('order_item_id', Integer, ForeignKey('order_items.id'), primary_key=True),
    Column('topping_id', Integer, ForeignKey('food_toppings.id'), primary_key=True)
)

class OrderItem(Base):
    __tablename__ = "order_items"

    # id = Column(Integer, primary_key=True, index=True)
    # order_id = Column(Integer, ForeignKey("orders.id"))
    # cart_item_id = Column(Integer, ForeignKey("cart_items.id"))

    # order = relationship("Order", back_populates="items")
    # cart_item = relationship("CartItem")

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    food_id = Column(Integer, ForeignKey("food.id"))
    food_name = Column(String)
    food_image = Column(String)
    quantity = Column(Integer)
    size_id = Column(Integer, ForeignKey("food_sizes.id"), nullable=True)
    size_name = Column(String, nullable=True)
    size_price = Column(Float, nullable=True)
    note = Column(String, nullable=True)

    order = relationship("Order", back_populates="items")
    food = relationship("Food")
    size = relationship("FoodSize")
    toppings = relationship(
        "FoodTopping",
        secondary=order_item_topping_table,
        backref="order_items"
    )
