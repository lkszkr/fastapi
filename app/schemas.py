from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr # walidacja danych, pydantic osobna paczka

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
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
    published: bool = True

class CreatePost(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None # powoduje blad gdy w create_token nie rzutuje sie na str


