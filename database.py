from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


from .config import get_settings

settings=get_settings()
DATABASE_URL=f"postresql://{settings.db_username}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
engine=create_engine(DATABASE_URL)
SessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)


Base=declarative_base()


def get_db():
    db=SessionLocal()
    try:
        yield db 
    finally:
        db.close()

    