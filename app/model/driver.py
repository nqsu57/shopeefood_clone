import enum
from sqlalchemy import Column, Integer, String, Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class Driver(Base):
    __tablename__ = "drivers"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    license_number = Column(String)
    vehicle_type = Column(String)
    license_plate = Column(String) 
    driver_license_number = Column(String)
    identity_card_number= Column(String)

    user = relationship("User", back_populates="driver_profile")
