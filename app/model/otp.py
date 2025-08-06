from sqlalchemy import Column, Integer, String, DateTime, Boolean, Index
from datetime import datetime, timedelta
from app.database.database  import Base

class OTP(Base):
    __tablename__ = "otps"
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, index=True)
    code = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_used = Column(Boolean, default=False)

    def is_expired(self):
        return datetime.utcnow() > self.created_at + timedelta(minutes=5)


    __table_args__ = (
        Index("ix_otp_phone_code", "phone", "code"),
    )