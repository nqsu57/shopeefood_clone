import random
import os
import re
from fastapi import HTTPException
from twilio.rest import Client
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
# from dotenv import load_dotenv
# from pathlib import Path


# env_path = Path(__file__).resolve().parents[2] / ".env"
# load_dotenv(dotenv_path=env_path)

def generate_otp_code() -> str:
    return f"{random.randint(100000, 999999)}"

def normalize_phone(phone: str) -> str:
    phone = phone.strip().replace(" ", "")

    # Remove all non-digit and '+' characters (an extra safety check)
    phone = re.sub(r"[^\d+]", "", phone)

    if phone.startswith("0") and len(phone) == 10:
        return "+84" + phone[1:]
    elif phone.startswith("84") and len(phone) == 11:
        return "+84" + phone[2:]
    elif phone.startswith("+84") and len(phone) == 12:
        return phone
    raise ValueError("Invalid phone number format")

def send_sms_mock(phone: str, otp: str):
    # In production, use Twilio or another provider
    print(f"Sending SMS to {phone}: Your OTP code is {otp}")

def send_sms(phone: str, otp: str):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_phone = os.getenv("TWILIO_PHONE_NUMBER")
    print("=== ENV CHECK ===")
    print("TWILIO_ACCOUNT_SID:", os.getenv("TWILIO_ACCOUNT_SID"))
    print("TWILIO_AUTH_TOKEN:", os.getenv("TWILIO_AUTH_TOKEN"))
    print("TWILIO_PHONE_NUMBER:", os.getenv("TWILIO_PHONE_NUMBER"))
    print("==================")
    if not all([account_sid, auth_token, twilio_phone]):
        raise HTTPException(status_code=500, detail="Twilio config missing in environment variables")

    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f"Your OTP code is {otp}",
            from_=twilio_phone,
            to=phone
        )
        print(f"[Twilio] Sent OTP to {phone} | SID: {message.sid}")
    except Exception as e:
        print(f"[Twilio Error] Failed to send SMS to {phone}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to send SMS")