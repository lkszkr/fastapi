from .database import Base
from sqlalchemy import TIMESTAMP, Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Payments(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, nullable=False)
    ammount = Column(Float, nullable=False)
    status = Column(Boolean, nullable=False, server_default="True")
    created_at = Column(TIMESTAMP(timezone=False), nullable=False, server_default=text("now()"))

    # ForeignKeys
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)

    post = relationship("Post", back_populates="payments")
    owner = relationship("User")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    goal = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=False), nullable=False, server_default=text("now()"))

    # ForeignKeys
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Base64 encoded data
    image = Column(String, nullable=True)

    payments = relationship("Payments", back_populates="post", cascade="all, delete-orphan") 
    owner = relationship("User") # Fetching data from User bellow 

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    image = image = Column(String, nullable=True, server_default=None)
    privileged = Column(Boolean, nullable=False, server_default="False")
    created_at = Column(TIMESTAMP(timezone=False), nullable=False, server_default=text("now()"))

    # post = relationship("Post")
    # payment = relationship("Payments")




