from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import cloudinary


from .config import get_settings

settings=get_settings()
cloudinary.config(
    cloud_name=settings.cloud_name,
    api_key=settings.cloud_api_key,
    api_secret=settings.cloud_secret,
    secure=True
)

DATABASE_URL = (
    f"postgresql://{settings.db_username}:{settings.db_password}"
    f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
)
engine=create_engine(DATABASE_URL)
SessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)


Base=declarative_base()


def get_db():
    db=SessionLocal()
    try:
        yield db 
    finally:
        db.close()

