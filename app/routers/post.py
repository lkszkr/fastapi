from typing import List, Optional
from fastapi import Depends, Response, status, HTTPException, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session, joinedload

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.Post], status_code=status.HTTP_200_OK) # Default way how response is supposed to look like
def get_posts(db: Session = Depends(get_db), search: Optional[str] = ""): # %20 - Space in url, 5 posts limit per response 

    # Without fetching payments data
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all()

    posts = db.query(models.Post).filter(models.Post.title.contains(search)).order_by(models.Post.id).options(joinedload(models.Post.payments)).all()
    
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) # Changing default status code
def create_posts(post: schemas.CreatePost, db: Session = Depends(get_db), current_user =  Depends(oauth2.get_current_user)): 
    
    # Base64 decode
    # image_data_bytes = None
    # if post.image is not None:
    #     image_data_bytes = base64.b64decode(post.image)
    #     #post.image = image_data_bytes
    
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # Equivalent of RETURNING from SQL

    return  new_post

#Using file Upload, can be deleted 
# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) # Changing default status code
# def create_posts(title: str = Form(), content: str = Form(), goal: float = Form(), image: UploadFile = File(default=None), db: Session = Depends(get_db), current_user =  Depends(oauth2.get_current_user)): 

#     os.makedirs("images", exist_ok=True)
#     if image is not None:
#         if isinstance("images", str) and isinstance(image.filename, str):
#             current_date = datetime.now()
#             new_filename = f"{current_date.strftime('%Y-%m-%d_%H-%M-%S')}-{title}.jpg"
#             image.filename = new_filename

#             # Get a valid file path using os.path.join
#             file_path = os.path.join("images", image.filename)
            
#             # Save the uploaded image to the specified directory
#             with open(file_path, "wb") as file:
#                 file.write(image.file.read())
#         else:
#             # Handle the case where upload_dir or image.filename is not a valid string
#             raise HTTPException(status_code=400, detail="Invalid upload_dir or image.filename")
#         new_post = models.Post(owner_id=current_user.id,title=title, content=content, goal=goal, image=new_filename)
#     else:
#         new_post = models.Post(owner_id=current_user.id,title=title, content=content, goal=goal)
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)

#     return  new_post

@router.get("/{id}", response_model=schemas.Post, status_code=status.HTTP_200_OK)
def get_post(id: int, db: Session = Depends(get_db)): # Validates and casts from str to int
    post = db.query(models.Post).filter(models.Post.id == id).options(joinedload(models.Post.payments)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} not found")

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
    deleted_post_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = deleted_post_query.first()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} not found")
    if deleted_post.owner_id != current_user.id and current_user.privileged == False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    deleted_post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post, status_code=status.HTTP_200_OK)
def update_post(id: int, post : schemas.CreatePost, db: Session = Depends(get_db), current_user =  Depends(oauth2.get_current_user)):
    updated_post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = updated_post_query.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} not found")
    #print(type(current_user.privileged))
    if updated_post.owner_id != current_user.id and current_user.privileged == False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    update_data = post.model_dump()

    # Old line which cased an error
    # updated_post_query.update(update_data, synchronize_session=False)

    # Convert the dictionary to the required format inline
    update_dict = {getattr(models.Post, key): value for key, value in update_data.items()}
    
    # Update the post
    updated_post_query.update(update_dict, synchronize_session=False)
    db.commit()
    
    return updated_post_query.first()