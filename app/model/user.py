import enum
from sqlalchemy import Column, Integer, String, Enum, Boolean
from sqlalchemy.orm import relationship
from app.database.database import Base

class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"
    driver = "driver"
    restaurant = "restaurant"

class UserStatus(str, enum.Enum):
    active = "active"
    locked = "locked"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    gender = Column(String, default="Default")
    hashed_password = Column(String, nullable=False)
    avatar_url = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)

    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus.active, nullable=False)
    restaurant_profile = relationship("Restaurant", back_populates="user", uselist=False)
    cart_items = relationship("CartItem", back_populates="user")
    addresses = relationship("Address", back_populates="user")
    driver_profile = relationship("Driver", back_populates="user", uselist=False)
