from datetime import datetime
import email
from typing import Optional, List
from pydantic import BaseModel, EmailStr, validator
#Pydantic validates data automaticly

class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str
    image: Optional[str] = None 
    @validator("name", "surname", "password", pre=True, always=True)
    def check_whitespace(cls, value):
        if not value.strip():
            raise ValueError("Field cannot be only spaces")
        return value

class UserOut(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr
    image: Optional[str]
    created_at: datetime
    privileged: bool
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Payment(BaseModel):
    id: int
    ammount: float
    status: bool
    created_at: datetime
    user_id: int
    post_id: int
    class Config:
        from_attributes = True

class CreatePayment(BaseModel):
    ammount: float
    @validator("ammount", pre=True, always=True)
    def check_greater_than_one(cls, value):
        if value <= 1.0:
            raise ValueError("Amount must be greater than 1.0")
        return value

class PostBase(BaseModel):
    title: str
    content: str
    goal: float
    image: Optional[str] = None

class CreatePost(PostBase):
    pass
    @validator("title", "content", pre=True, always=True)
    def check_whitespace(cls, value):
        if not value.strip():
            raise ValueError("Field cannot be only spaces")
        return value

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    payments: List[Payment]
    owner: UserOut
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    # Cases error when it is not casted as string in create_token
    id: Optional[str] = None
    privileged: Optional[bool] = None

class AdminPost(BaseModel):
    id: int
    title: str
    owner_id: int
    created_at: datetime

class AdminUser(UserOut):
    pass