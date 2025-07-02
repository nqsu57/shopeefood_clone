from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.database.database import get_db
from sqlalchemy.orm import Session
from app.crud import address as crud_address
from typing import List
from app.schemas.address import ProvinceOut, DistrictOut, WardOut, AddressOut, AddressCreate
from app.core.security import get_current_user
from app.model.user import User



address_router = APIRouter()

@address_router.get("/provinces", response_model=List[ProvinceOut])
def read_provinces(db: Session = Depends(get_db)):
    return crud_address.get_provinces(db)


@address_router.get("/provinces/{province_id}/districts", response_model=List[DistrictOut])
def read_districts(province_id: int, db: Session = Depends(get_db)):
    return crud_address.get_districts_by_province(db, province_id)


@address_router.get("/districts/{district_id}/wards", response_model=List[WardOut])
def read_wards(district_id: int, db: Session = Depends(get_db)):
    return crud_address.get_wards_by_district(db, district_id)



@address_router.get("/address", response_model=List[AddressOut])
def get_address_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return crud_address.get_addresses(db, current_user.id)


@address_router.post("/address", response_model=AddressOut)
def create_address(
    address: AddressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return crud_address.create_address(db, current_user.id, address)


@address_router.delete("/address/{address_id}")
def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    addr = crud_address.delete_address(db, current_user.id, address_id)
    if not addr:
        raise HTTPException(status_code=404, detail="Address not found")
    return {"detail": "Address deleted"}


@address_router.put("/address/{address_id}/set_default")
def set_default_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated = crud_address.set_default_address(db, current_user.id, address_id)
    return updated
