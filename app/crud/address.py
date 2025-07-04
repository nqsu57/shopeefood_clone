from sqlalchemy.orm import Session, joinedload
from app.model.address import Province, District, Ward, Address
from app.schemas.address import AddressCreate

def get_provinces(db: Session):
    return db.query(Province).all()


def get_districts_by_province(db: Session, province_id: int):
    return db.query(District).filter(District.province_id == province_id).all()


def get_wards_by_district(db: Session, district_id: int):
    return db.query(Ward).filter(Ward.district_id == district_id).all()


def get_addresses(db: Session, user_id: int):
    return (
        db.query(Address)
        .options(
            joinedload(Address.province),
            joinedload(Address.district),
            joinedload(Address.ward)
        )
        .filter(Address.user_id == user_id)
        .all()
    )

def create_address(db: Session, user_id: int, address: AddressCreate):
    is_first = db.query(Address).filter(Address.user_id == user_id).count() == 0
    if address.is_default or is_first:
        db.query(Address).filter(Address.user_id == user_id).update({Address.is_default: False})

    new_address = Address(
        user_id=user_id,
        recipient_name=address.recipient_name,
        phone_number=address.phone_number,
        address_line=address.address_line,
        province_id=address.province_id,
        district_id=address.district_id,
        ward_id=address.ward_id,
        label=address.label,
        is_default=address.is_default or is_first
    )
    db.add(new_address)
    db.commit()
    db.refresh(new_address)

    # Truy vấn lại để lấy đầy đủ thông tin quan hệ
    return (
        db.query(Address)
        .options(
            joinedload(Address.province),
            joinedload(Address.district),
            joinedload(Address.ward)
        )
        .filter(Address.id == new_address.id)
        .first()
    )

def update_address(db: Session, user_id: int, address_id: int, data: AddressCreate):
    addr = db.query(Address).filter(
        Address.id == address_id, Address.user_id == user_id
    ).first()
    if not addr:
        return None

    if data.is_default:
        db.query(Address).filter(Address.user_id == user_id).update({Address.is_default: False})

    addr.recipient_name = data.recipient_name
    addr.phone_number = data.phone_number
    addr.address_line = data.address_line
    addr.province_id = data.province_id
    addr.district_id = data.district_id
    addr.ward_id = data.ward_id
    addr.label = data.label
    addr.is_default = data.is_default or addr.is_default

    db.commit()
    db.refresh(addr)
    return addr



def delete_address(db: Session, user_id: int, address_id: int):
    addr = db.query(Address).filter(
        Address.id == address_id, Address.user_id == user_id
    ).first()
    if addr:
        db.delete(addr)
        db.commit()
    return addr


def set_default_address(db: Session, user_id: int, address_id: int):
    addr = db.query(Address).filter(Address.id == address_id, Address.user_id == user_id).first()
    if not addr:
        return {"detail": "Address not found"}

    db.query(Address).filter(Address.user_id == user_id).update({Address.is_default: False})

    addr.is_default = True
    db.commit()
    db.refresh(addr)

    return {"detail": "Default address updated", "address_id": addr.id}