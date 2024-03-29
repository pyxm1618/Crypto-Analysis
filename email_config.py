import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 邮件服务配置
SMTP_SERVER = 'smtp.163.com'
SMTP_PORT = 25
FROM_EMAIL = '*****发件邮箱******'
TO_EMAIL = '*****收件邮箱******'
SMTP_AUTH_PASSWORD = '*****邮箱授权码******'

def send_email(subject, body, to_email, from_email, smtp_auth_password):
    try:
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(from_email, smtp_auth_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("邮件发送成功！")
    except Exception as e:
        print(f"邮件发送失败：{e}")
