from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    payment_method = Column(String, default="COD")
    shipping_fee = Column(Integer, default=0)
    total = Column(Float, default=0)

    user = relationship("User")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    cart_item_id = Column(Integer, ForeignKey("cart_items.id"))

    order = relationship("Order", back_populates="items")
    cart_item = relationship("CartItem")
