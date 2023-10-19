from datetime import datetime
from pydantic import BaseModel, EmailStr # walidacja danych, pydantic osobna paczka

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
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True
