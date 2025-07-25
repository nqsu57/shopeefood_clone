from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, Table, MetaData, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from app.database.database import Base

class Dish(Base):
    __tablename__ = "dish"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    brand = Column(String)

    