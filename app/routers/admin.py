from fastapi import APIRouter, Depends, HTTPException, status, Response
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schemas, oauth2, models
from typing import List


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/posts", response_model=List[schemas.AdminPost], status_code=status.HTTP_200_OK)
def admin_get_posts(db: Session = Depends(get_db), current_user =  Depends(oauth2.get_current_user)):
    if not current_user.privileged:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    posts = db.query(models.Post).all()
    return posts

@router.get("/users", response_model=List[schemas.AdminUser], status_code=status.HTTP_200_OK)
def admin_get_users(db: Session = Depends(get_db), current_user =  Depends(oauth2.get_current_user)):
    if not current_user.privileged:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    users = db.query(models.User).all()
    return users

@router.delete("/users/{id}")
def delete_user(id: int, db: Session = Depends(get_db), current_user =  Depends(oauth2.get_current_user)):
    if not current_user.privileged:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    deleted_user_query = db.query(models.User).filter(models.User.id == id)
    #deleted_user = deleted_user_query.first()
    if deleted_user_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} not found")
    deleted_user_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
