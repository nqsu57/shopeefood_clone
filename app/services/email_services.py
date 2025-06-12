import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Đọc biến môi trường từ .env

MAILERSEND_API_KEY = os.getenv("MAILERSEND_API_KEY")
MAIL_FROM = "no-reply@yourdomain.com"

def send_reset_email_mailersend(to_email: str, token: str):
    reset_link = f"http://localhost:8000/reset-password?token={token}"
    subject = "Đặt lại mật khẩu"
    text = f"Chào bạn,\n\nVui lòng click vào liên kết sau để đặt lại mật khẩu của bạn:\n{reset_link}\n\nNếu bạn không yêu cầu, hãy bỏ qua email này."

    headers = {
        "Authorization": f"Bearer {MAILERSEND_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "from": {
            "email": MAIL_FROM,
            "name": "Your App"
        },
        "to": [
            {
                "email": to_email,
                "name": "Người dùng"
            }
        ],
        "subject": subject,
        "text": text
    }

    response = requests.post("https://api.mailersend.com/v1/email", json=data, headers=headers)

    if response.status_code != 202:
        print("Gửi email thất bại:", response.text)
        raise Exception("Gửi email thất bại")
    else:
        print("Gửi email thành công")
