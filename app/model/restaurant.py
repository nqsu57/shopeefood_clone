from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    foods = relationship("Food", back_populates="restaurant")
    user = relationship("User", back_populates="restaurant_profile")