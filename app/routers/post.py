from typing import List
from fastapi import Depends, Response, status, HTTPException, APIRouter
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts # Automatyczna serializacja

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) # zmienia domyslny status code
def create_posts(post: schemas.CreatePost, db: Session = Depends(get_db)): # Body(...) wszystkie pola z body requesta przetwarza do slownika i zapisuje w payloads
    # print(post.rating)
    # print(post.model_dump()) # konwertuje na slownik
    # post_dict = post.model_dump()
    # post_dict['id'] = randrange(2,1000000)
    # my_posts.append(post_dict)
    
    # cursor.execute("""INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # RETURINING z sql
    return  new_post

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)): # Waliduje i rzutuje z str na int , resposne juz nie potrzebny przy raise HTTPexception, usuniete response: Response
    # post = find_post(id)
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with {id} not found"}
    # print(post)
    return post

@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()

    #index = find_index_post(id)
    
    deleted_post_query = db.query(models.Post).filter(models.Post.id == id)
    if deleted_post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} not found")
    #my_posts.pop(index)
    # conn.commit()
    deleted_post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post : schemas.CreatePost, db: Session = Depends(get_db)):
    #index = find_index_post(id)
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()

    updated_post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = updated_post_query.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} not found")
    updated_post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    # post_dict = post.model_dump()
    # post_dict["id"] = id
    # my_posts[index] = post_dict
    # conn.commit()
    
    return updated_post_query.first()