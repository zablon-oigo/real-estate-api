import sqlalchemy as sql
from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text


class User(Base):
    __tablename__ = "users"

    id = sql.Column(sql.Integer, primary_key=True, index=True)
    email = sql.Column(sql.String(255), unique=True, index=True, nullable=False)
    password = sql.Column(sql.String, nullable=False)
    is_active = sql.Column(sql.Boolean, default=True)
    is_verified = sql.Column(sql.Boolean, default=False)
    date_joined = sql.Column(sql.TIMESTAMP(timezone=True), server_default=text('now()'))

    profile = relationship("AgentDetails", uselist=False, back_populates="user")
    otps = relationship("UserOneTimePassword", back_populates="user", cascade="all, delete")

    def __repr__(self):
        return f"<User id={self.id} email={self.email} verified={self.is_verified}>"


class UserOneTimePassword(Base):
    __tablename__ = "user_otp"

    id = sql.Column(sql.Integer, autoincrement=True, primary_key=True, index=True)
    user_id = sql.Column(sql.Integer, sql.ForeignKey("users.id", ondelete="CASCADE"))
    code = sql.Column(sql.String(6), unique=True, nullable=False)
    is_valid = sql.Column(sql.Boolean, default=True)

    user = relationship("User", back_populates="otps")

    def __repr__(self):
        return f"<OTP code={self.code} valid={self.is_valid}>"


class AgentDetails(Base):
    __tablename__ = "agents"

    id = sql.Column(sql.Integer, autoincrement=True, primary_key=True, index=True)
    names = sql.Column(sql.String, nullable=False)
    phone_number = sql.Column(sql.String(20), nullable=False)
    office_address = sql.Column(sql.String)
    profile_img = sql.Column(sql.String, nullable=True)
    user_id = sql.Column(sql.Integer, sql.ForeignKey("users.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="profile")

    def __repr__(self):
        return f"<Agent id={self.id} name={self.names}>"
