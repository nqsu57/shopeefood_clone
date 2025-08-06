from pydantic import BaseModel
from typing import Optional

class DriverOut(BaseModel):
    license_number: Optional[str]
    vehicle_type: Optional[str]
    license_plate: Optional[str]
    driver_license_number: Optional[str]
    identity_card_number: Optional[str]
