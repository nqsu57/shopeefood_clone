from sqlalchemy.orm import Session
from app.model.address import Province, District, Ward, Address
from app.schemas.address import AddressCreate

def get_provinces(db: Session):
    return db.query(Province).all()


def get_districts_by_province(db: Session, province_id: int):
    return db.query(District).filter(District.province_id == province_id).all()


def get_wards_by_district(db: Session, district_id: int):
    return db.query(Ward).filter(Ward.district_id == district_id).all()



def get_addresses(db: Session, user_id: int):
    return db.query(Address).filter(Address.user_id == user_id).all()


def create_address(db: Session, user_id: int, address: AddressCreate):
    is_first = db.query(Address).filter(Address.user_id == user_id).count() == 0
    new_address = Address(
        user_id=user_id,
        recipient_name=address.recipient_name,
        phone_number=address.phone_number,
        address_line=address.address_line,
        province_id=address.province_id,
        district_id=address.district_id,
        ward_id=address.ward_id,
        is_default=address.is_default if address.is_default else is_first
    )
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address


def delete_address(db: Session, user_id: int, address_id: int):
    addr = db.query(Address).filter(
        Address.id == address_id, Address.user_id == user_id
    ).first()
    if addr:
        db.delete(addr)
        db.commit()
    return addr


def set_default_address(db: Session, user_id: int, address_id: int):
    addresses = db.query(Address).filter(Address.user_id == user_id).all()
    for addr in addresses:
        addr.is_default = addr.id == address_id
    db.commit()
    return db.query(Address).filter(Address.user_id == user_id).all()