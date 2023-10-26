from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr # walidacja danych, pydantic osobna paczka

class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Walidacja automatyczna z pydantic
class PostBase(BaseModel):
    title: str
    content: str
    goal: float
    #published: bool = True

class CreatePost(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    class Config:
        from_attributes = True

class CreatePayment(BaseModel):
    ammount: float

class Payment(BaseModel):
    id: int
    ammount: float
    status: bool
    user_id: int
    post_id: int
    user: UserOut
    post: PostBase
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None # powoduje blad gdy w create_token nie rzutuje sie na str


