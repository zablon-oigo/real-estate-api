from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr = Field(..., title="User email address", example="test@mail.com")


class UserCreate(UserBase):
    password: str = Field(..., title="User password", example="strong password")


class User(UserBase):
    id: int
    is_active: bool
    is_verified: bool

    class Config:
        orm_mode = True


class OTPData(BaseModel):
    user_id: int
    code: str

    class Config:
        orm_mode = True


class OneTimePassword(BaseModel):
    code: str


class TokenData(BaseModel):
    user_id: Optional[str] = None


class ForgetPassword(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    token: str
    password: str
    confirm_password: str

    @model_validator(mode='after')
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self

    class Config:
        orm_mode = True


class AgentBase(BaseModel):
    names:str
    phone_number:str
    office_address:str 



class AgentCreate(AgentBase):
    pass


class Agent(AgentBase):
    id:int 
    profile: Union[str,None]=None 
    user: User  