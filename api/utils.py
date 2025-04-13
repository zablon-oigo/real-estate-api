from passlib.context import CryptContext
from .config import get_settings
pwd_context=CryptContext(schemes=['bcrypt'])
from fastapi import BackgroundTasks 
from typing import List
from fastapi_mail import ConnectionConfig,FastMail, MessageSchema 
from passlib.context import CryptContext
import pyotp
settings = get_settings()
conf = ConnectionConfig(
    MAIL_USERNAME=f"{settings.mail_username}",
    MAIL_PASSWORD=f"{settings.mail_password}",
    MAIL_FROM=f"{settings.mail_from}",
    MAIL_PORT=587,
    MAIL_SERVER=f"{settings.mail_server}",
    MAIL_STARTTLS=True,  
    MAIL_SSL_TLS=False,  
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

def send_mail(background_task:BackgroundTasks, subject:str, recipient:List, message:str):
    message=MessageSchema(
        subject=subject,
        recipients=recipient,
        body=message,
        subtype="html"
    )
    fm=FastMail(conf)
    background_task.add_task(fm.send_message,message)

def hash_password(password:str):
    return pwd_context.hash(password)


def verify_password(rw_password:str, hashed_password:str):
    return pwd_context.verify(rw_password, hashed_password) 



secret=pyotp.random_base32()
time_otp=pyotp.TOTP(secret, interval=120)

def generate_otp_code():
    otp=time_otp.now()
    return otp 


def verify_otp(code):
    return time_otp.verify(code)
