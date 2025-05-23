import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
import os
import socks
import socket

# 加载.env文件中的环境变量
load_dotenv()

# 设置代理（仅在https_proxy环境变量存在且格式正确时启用）
proxy = os.getenv("https_proxy")
if proxy and isinstance(proxy, str):
    if proxy.startswith("http://"):
        proxy = proxy[7:]
    try:
        host, port = proxy.split(":")
        socks.set_default_proxy(socks.HTTP, host, int(port))
        socket.socket = socks.socksocket
    except (ValueError, AttributeError):
        print("警告: https_proxy环境变量格式不正确，忽略代理设置")


def send(title, body, files):
    sender = os.getenv("EMAIL_SENDER")
    assert sender, "发件人邮箱不能为空"
    receiver = os.getenv("EMAIL_RECV")
    password = os.getenv("EMAIL_PASSWORD")
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = title
    msg.attach(MIMEText(body, "html"))

    if files:
        for file in files:
            try:
                with open(file, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename={file.split('/')[-1]}",
                    )
                    msg.attach(part)
            except FileNotFoundError:
                print(f"文件 {file} 不存在，跳过该附件。")

    server = smtplib.SMTP(os.getenv("EMAIL_SMTP"), os.getenv("EMAIL_PORT"))
    server.starttls()  # 启动TLS模式
    server.login(sender, password)
    text = msg.as_string()
    server.sendmail(sender, receiver, text)
    server.quit()
