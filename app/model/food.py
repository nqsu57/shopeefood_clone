from sqlalchemy import Column, Integer, String, ForeignKey
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