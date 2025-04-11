import pathlib
from pydantic_settings import BaseSettings
from dotenv import load_dotenv 

load_dotenv()

class Settings(BaseSettings):
    db_host:str
    db_port:int 
    db_username:str 
    db_password:str 
    db_name:str 


    class Config:
        env_file=f"{pathlib.Path(__file__).resolve().parent}/.env"


def get_settings():
    return Settings()


get_settings()