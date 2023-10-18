from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel # walidacja danych, pydantic osobna paczka 
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

get_db()

# Walidacja automatyczna z pydantic
class Post(BaseModel): 
    title: str
    content: str
    published: bool = True

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
my_posts = [
    {"id": 1, "title": "title 1", "content": "content 1"},
    {"id": 2, "title": "title 2", "content": "content 2"}
]
# niepotrzebne
def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post

def find_index_post(id):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts} # Automatyczna serializacja

@app.post("/posts", status_code=status.HTTP_201_CREATED) # zmienia domyslny status code
def create_posts(post: Post): # Body(...) wszystkie pola z body requesta przetwarza do slownika i zapisuje w payloads
    # print(post.rating)
    # print(post.model_dump()) # konwertuje na slownik
    # post_dict = post.model_dump()
    # post_dict['id'] = randrange(2,1000000)
    # my_posts.append(post_dict)
    cursor.execute("""INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return  {"post": new_post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response): # Waliduje i rzutuje z str na int , resposne juz nie potrzebny przy raise HTTPexception
    # post = find_post(id)
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with {id} not found"}
    print(post)
    return {"post detail": post}

@app.delete("/posts/{id}")
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deleted_post = cursor.fetchone()

    #index = find_index_post(id)
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} not found")
    #my_posts.pop(index)
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post : Post):
    #index = find_index_post(id)
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} not found")
    # post_dict = post.model_dump()
    # post_dict["id"] = id
    # my_posts[index] = post_dict
    conn.commit()
    return {"message": updated_post}
