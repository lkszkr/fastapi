from typing import List, Optional
from fastapi import Depends, Response, status, HTTPException, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.Post]) # w jaki sposob ma byc domysle zwrocony request od api
def get_posts(db: Session = Depends(get_db), limit: int = 5, search: Optional[str] = ""): #%20 - spacja w url, limit 5 postow 
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all()
    return posts # Automatyczna serializacja

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) # zmienia domyslny status code
def create_posts(post: schemas.CreatePost, db: Session = Depends(get_db), current_user =  Depends(oauth2.get_current_user)): # Body(...) wszystkie pola z body requesta przetwarza do slownika i zapisuje w payloads
    # print(post.rating)
    # print(post.model_dump()) # konwertuje na slownik
    # post_dict = post.model_dump()
    # post_dict['id'] = randrange(2,1000000)
    # my_posts.append(post_dict)
    print(current_user.id) # dostep do pol user (moze byc blad)
    # cursor.execute("""INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
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

@router.post("/{id}/payment", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Payment)
def create_payment(id: int, payment: schemas.CreatePayment, db: Session = Depends(get_db), current_user =  Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} not found")
    new_payment = models.Payments(user_id=current_user.id, post_id=id, **payment.model_dump())
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment

@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user =  Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()

    #index = find_index_post(id)
    
    deleted_post_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = deleted_post_query.first()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} not found")
    #my_posts.pop(index)
    # conn.commit()
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    deleted_post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post : schemas.CreatePost, db: Session = Depends(get_db), current_user =  Depends(oauth2.get_current_user)):
    #index = find_index_post(id)
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()

    updated_post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = updated_post_query.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} not found")
    
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    updated_post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    # post_dict = post.model_dump()
    # post_dict["id"] = id
    # my_posts[index] = post_dict
    # conn.commit()
    
    return updated_post_query.first()