import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

MAILTRAP_HOST = "sandbox.smtp.mailtrap.io"
MAILTRAP_PORT = 587
MAILTRAP_USERNAME = "07c7c52310e470"
MAILTRAP_PASSWORD = "bf13cc059635a3" 

FROM_EMAIL = "no-reply@shopeefood.vn"


def send_reset_password_email_test(to_email: str, reset_link: str):
    subject = "Yêu cầu đặt lại mật khẩu"
    html_content = f"""
        <h3>Đặt lại mật khẩu</h3>
        <p>Bạn vừa yêu cầu đặt lại mật khẩu. Nhấn vào liên kết bên dưới để tiếp tục:</p>
        <a href="{reset_link}">Đặt lại mật khẩu</a>
        <p>Nếu bạn không yêu cầu, vui lòng bỏ qua email này.</p>
    """

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP(MAILTRAP_HOST, MAILTRAP_PORT) as server:
        server.login(MAILTRAP_USERNAME, MAILTRAP_PASSWORD)
        server.send_message(msg)
