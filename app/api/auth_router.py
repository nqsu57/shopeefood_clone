from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import RequestOTP, VerifyOTP
from app.model.user import User
from app.model.otp import OTP
from app.crud.auth import generate_otp_code, send_sms_mock, send_sms, normalize_phone
from app.core.security import create_access_token
from app.database.database import get_db
from datetime import datetime


auth_router = APIRouter()

@auth_router.post("/auth/request-otp")
def request_otp(data: RequestOTP, db: Session = Depends(get_db)):
    input_phone = data.phone.strip()
    print(f"[DEBUG][request_otp] Raw input phone: {input_phone}")

    # 1. Normalize phone trước
    try:
        normalized_phone = normalize_phone(input_phone)
        print(f"[DEBUG][request_otp] Normalized phone: {normalized_phone}")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid phone number format")

    # 2. Kiểm tra user tồn tại với số normalized
    user = db.query(User).filter(User.phone == normalized_phone).first()
    if not user:
        print(f"[DEBUG][request_otp] User not found with phone: {normalized_phone}")
        raise HTTPException(status_code=404, detail="Phone number not registered")

    # 3. Sinh mã OTP
    otp_code = generate_otp_code()
    print(f"[DEBUG][request_otp] Generated OTP: {otp_code}")

    # 4. Gửi OTP
    try:
        send_sms(normalized_phone, otp_code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send OTP: {str(e)}")

    # 5. Lưu OTP vào DB
    otp_entry = OTP(
        phone=normalized_phone,
        code=otp_code,
        created_at=datetime.utcnow(),
        is_used=False
    )
    db.add(otp_entry)
    db.commit()
    
    print(f"[DEBUG][request_otp] OTP saved to DB for phone: {normalized_phone}")

    return {"message": "OTP sent successfully"}

@auth_router.post("/auth/verify-otp")
def verify_otp(data: VerifyOTP, db: Session = Depends(get_db)):
    print(f"[DEBUG][verify_otp] Input phone: {data.phone}, Input OTP: {data.otp}")
    # 1. Normalize phone
    try:
        normalized_phone = normalize_phone(data.phone)
        print(f"[DEBUG][verify_otp] Normalized phone: {normalized_phone}")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid phone number format")

    # 2. Truy vấn OTP gần nhất hợp lệ
    otp = (
        db.query(OTP)
        .filter(
            OTP.phone == normalized_phone,
            OTP.code == data.otp,
            OTP.is_used == False
        )
        .order_by(OTP.created_at.desc())
        .first()
    )

    # if not otp or otp.is_expired():
    #     print(f"[DEBUG][verify_otp] OTP not found or already used for phone: {normalized_phone}")
    #     raise HTTPException(status_code=401, detail="Invalid or expired OTP")
    if not otp:
        print(f"[DEBUG][verify_otp] OTP not found or already used for phone: {normalized_phone}")
        raise HTTPException(status_code=401, detail="Invalid or expired OTP")

    if otp.is_expired():
        print(f"[DEBUG][verify_otp] OTP expired. Created at: {otp.created_at}")
        raise HTTPException(status_code=401, detail="Invalid or expired OTP")

    # 3. Đánh dấu OTP đã dùng
    otp.is_used = True
    db.commit()
    print(f"[DEBUG][verify_otp] OTP verified successfully for phone: {normalized_phone}")

    # 4. Tìm user theo số điện thoại
    user = db.query(User).filter(User.phone == normalized_phone).first()
    print(f"user", user)
    
    if not user:
        print(f"[DEBUG][verify_otp] User not found with normalized phone: {normalized_phone}")
        raise HTTPException(status_code=404, detail="User not found")

    # 5. Tạo JWT token
    token = create_access_token(data={"sub": user.phone})
    print(f"[DEBUG][verify_otp] Token created for phone: {user.phone}")

    return {"access_token": token, "token_type": "bearer"}