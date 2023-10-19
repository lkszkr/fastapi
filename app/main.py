from fastapi import FastAPI 
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session

from .routers import post,user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

get_db()


while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="admin", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succsesfull!")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(2)

# hardcoded data
# my_posts = [
#     {"id": 1, "title": "title 1", "content": "content 1"},
#     {"id": 2, "title": "title 2", "content": "content 2"}
# ]
# niepotrzebne
# def find_post(id):
#     for post in my_posts:
#         if post["id"] == id:
#             return post

# def find_index_post(id):
#     for index, post in enumerate(my_posts):
#         if post["id"] == id:
#             return index


@app.get("/")
def root():
    return {"message": "Hello World"}

app.include_router(post.router)
app.include_router(user.router)


