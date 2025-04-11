from pydantic import BaseModel,Field,EmailStr 

class UserBase(BaseModel):
    email:EmailStr=Field(..., title="user email address",example="test@mail.com")

class UserCreate(UserBase):
    password:str=Field(...,title="user password", example="strong password") 

class User(UserBase):
    id:int
    is_active:bool 
    is_verified:bool 