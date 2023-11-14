from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine, get_db
from .routers import post, user, auth, admin

models.Base.metadata.create_all(bind=engine) # Creates database
app = FastAPI()

get_db()

# Old code using SQL queries not SQLAlchemy
# while True:
#     try:
#         conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="admin", cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was succsesfull!")
#         break
#     except Exception as error:
#         print("Connection to database failed")
#         print("Error: ", error)
#         time.sleep(2)

# hardcoded data
# my_posts = [
#     {"id": 1, "title": "title 1", "content": "content 1"},
#     {"id": 2, "title": "title 2", "content": "content 2"}
# ]
# not needed
# def find_post(id):
#     for post in my_posts:
#         if post["id"] == id:
#             return post

# def find_index_post(id):
#     for index, post in enumerate(my_posts):
#         if post["id"] == id:
#             return index

origins = [
    "http://localhost:8080/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello World"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(admin.router)


