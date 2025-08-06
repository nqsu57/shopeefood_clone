import requests
import os
import httpx

MAILERSEND_API_KEY = os.getenv("MAILERSEND_API_KEY")
MAILERSEND_SENDER = os.getenv("MAILERSEND_SENDER")

def send_reset_password_email(to_email: str, reset_link: str):
    print(f"[MAILERSEND_SENDER] Send email:", MAILERSEND_SENDER)
    print(f"[MAILERSEND_API_KEY] Send email:", MAILERSEND_API_KEY)

    subject = "Đặt lại mật khẩu tài khoản của bạn"
    html_content = f"""
    <html>
    <body>
        <p>Xin chào,</p>
        <p>Bạn vừa yêu cầu đặt lại mật khẩu. Hãy nhấn vào nút bên dưới để tiếp tục:</p>
        <a href="{reset_link}" style="background:#007bff;color:white;padding:10px 20px;text-decoration:none;border-radius:5px;">Đặt lại mật khẩu</a>
        <p>Nếu bạn không thực hiện yêu cầu này, hãy bỏ qua email này.</p>
    </body>
    </html>
    """
    headers = {
        "Authorization": f"Bearer {MAILERSEND_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "from": {
            "email": MAILERSEND_SENDER,
            "name": "ShopeeFood Clone Support"
        },
        "to": [{"email": to_email}],
        "subject": subject,
        "html": html_content,
    }

    try:
        response = httpx.post("https://api.mailersend.com/v1/email", json=payload, headers=headers)
        response.raise_for_status()
        print(f"[MailerSend] Email sent to {to_email}")
    except httpx.HTTPStatusError as e:
        print(f"[MailerSend ERROR] Failed to send email: {e.response.text}")
