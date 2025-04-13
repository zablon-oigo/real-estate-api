import pathlib
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_username: str
    db_password: str
    db_name: str
    mail_username: str
    mail_password: str
    mail_from: str
    mail_server: str

    class Config:
        env_file = f"{pathlib.Path(__file__).resolve().parent}/.env"

def get_settings():
    return Settings()
