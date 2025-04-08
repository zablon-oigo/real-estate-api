import sqlalchemy as sql
from .database import Base
from sqlalchemy.orm import relationship 
from sqlalchemy.sql.expression import text 


class User(Base):
    __tablename__="users"
    id=sql.Column(sql.Integer, primary_key=True, index=True)
    email=sql.Column(sql.String(255), unique=True, index=True)
    password=sql.Colum(sql.String, nullable=False)
    is_active=sql.Column(sql.Boolean, default=True)
    is_verified=sql.Column(sql.Boolean, default=False)
    date_joined=sql.Column(sql.TIMESTAMP(timezone=True),server_default=text('now()'))
    