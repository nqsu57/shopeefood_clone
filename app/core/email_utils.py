import requests
import os

MAILERSEND_API_KEY = os.getenv("MAILERSEND_API_KEY")
FROM_EMAIL = "sungo.work@gmail.com"
FROM_NAME = "Reset Password"

def send_reset_email(to_email: str, reset_link: str):
    url = "https://api.mailersend.com/v1/email"
    headers = {
        "Authorization": f"Bearer {MAILERSEND_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "from": {"email": FROM_EMAIL, "name": FROM_NAME},
        "to": [{"email": to_email}],
        "subject": "Đặt lại mật khẩu",
        "html": f"""
            <h2>Yêu cầu đặt lại mật khẩu</h2>
            <p>Click vào liên kết bên dưới để đặt lại mật khẩu:</p>
            <a href="{reset_link}" style="padding:10px 20px;background:#4CAF50;color:#fff;text-decoration:none;border-radius:5px;">Đặt lại mật khẩu</a>
            <p>Liên kết có hiệu lực trong 15 phút.</p>
        """,
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 202:
        raise Exception(f"Failed to send email: {response.text}")

