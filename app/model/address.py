from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.database import Base

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    recipient_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    address_line = Column(String, nullable=False)   # Số nhà, tên đường

    province_id = Column(Integer, ForeignKey("provinces.id"))
    district_id = Column(Integer, ForeignKey("districts.id"))
    ward_id = Column(Integer, ForeignKey("wards.id"))

    is_default = Column(Boolean, default=False)

    user = relationship("User", back_populates="addresses")
    province = relationship("Province")
    district = relationship("District")
    ward = relationship("Ward")
    orders = relationship("Order", back_populates="address")


class Province(Base):
    __tablename__ = "provinces"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    districts = relationship("District", back_populates="province")


class District(Base):
    __tablename__ = "districts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    province_id = Column(Integer, ForeignKey("provinces.id"))

    province = relationship("Province", back_populates="districts")
    wards = relationship("Ward", back_populates="district")


class Ward(Base):
    __tablename__ = "wards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    district_id = Column(Integer, ForeignKey("districts.id"))

    district = relationship("District", back_populates="wards")
