from fastapi import Depends, status, HTTPException, APIRouter
from .. import models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session, joinedload
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# To delete
# @router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut) # Changes default status code
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), ):
    
#     if db.query(models.User).filter(models.User.email == user.email).first():
#         raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Email already exists")
#     user.password = utils.hash(user.password)
#     new_user = models.User(**user.model_dump())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return new_user

@router.get("/myuser", response_model=schemas.UserOut, status_code=status.HTTP_200_OK)
def get_my_user(db: Session = Depends(get_db),  current_user =  Depends(oauth2.get_current_user)):
    my_user_data = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not my_user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User data does not exist")
    return my_user_data

@router.put("/myuser", response_model=schemas.UserOut, status_code=status.HTTP_200_OK)
def update_my_user(user: schemas.UserCreate, db: Session = Depends(get_db),  current_user =  Depends(oauth2.get_current_user)):
    my_user_data = db.query(models.User).filter(models.User.id == current_user.id)
    existing_user = my_user_data.first()
    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user_email = str(existing_user.email)

    # Checking if email already exists in the database
    if user_email != user.email and db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Email already exists")
    # if db.query(models.User).filter(models.User.email == user.email).first():
    #     raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Email already exists")
    # Getting data of current logged user
    user.password = utils.hash(user.password)
    new_user_data = user.model_dump()
    update_dict = {getattr(models.User, key): value for key, value in new_user_data.items()}
    my_user_data.update(update_dict, synchronize_session=False)
    db.commit()
    return my_user_data.first()

@router.get("/myuser/myposts", response_model=List[schemas.Post], status_code=status.HTTP_200_OK)
def get_my_posts(db: Session = Depends(get_db), current_user =  Depends(oauth2.get_current_user)):
    my_posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).options(joinedload(models.Post.payments)).all()
    return my_posts

@router.get("/myuser/mypayments", response_model=List[schemas.Payment], status_code=status.HTTP_200_OK)
def get_my_payments(db: Session = Depends(get_db), current_user =  Depends(oauth2.get_current_user)):
    my_payments = db.query(models.Payments).filter(models.Payments.user_id == current_user.id).all()
    return my_payments  

# ?????
@router.get("/{id}",response_model=schemas.UserOut, status_code=status.HTTP_200_OK)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    
    return user