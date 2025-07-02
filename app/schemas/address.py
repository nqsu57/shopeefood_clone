from pydantic import BaseModel
from typing import List, Optional


class WardOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class DistrictOut(BaseModel):
    id: int
    name: str
    wards: List[WardOut] = []

    class Config:
        orm_mode = True


class ProvinceOut(BaseModel):
    id: int
    name: str
    districts: List[DistrictOut] = []

    class Config:
        orm_mode = True

class AddressCreate(BaseModel):
    recipient_name: str
    phone_number: str
    address_line: str
    province_id: int
    district_id: int
    ward_id: int
    is_default: Optional[bool] = False


class AddressOut(AddressCreate):
    id: int
    province: ProvinceOut
    district: DistrictOut
    ward: WardOut

    class Config:
        orm_mode = True


