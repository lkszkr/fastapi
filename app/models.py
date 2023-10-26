import email
from turtle import title
from .database import Base
from sqlalchemy import TIMESTAMP, Boolean, Column, Float, ForeignKey, Integer, Nullable, String
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Payments(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, nullable=False)
    ammount = Column(Float, nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    created_at = Column(TIMESTAMP(timezone=False), nullable=False, server_default=text("now()"))

    #ForeignKeys
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User")
    post = relationship("Post")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    goal = Column(Float, nullable=False)
    #published = Column(Boolean, server_default="True",nullable=False )
    created_at = Column(TIMESTAMP(timezone=False), nullable=False, server_default=text("now()"))

    #ForeignKeys
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User") # fetching data from User bellow 

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=False), nullable=False, server_default=text("now()"))


