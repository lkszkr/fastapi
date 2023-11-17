from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm 
from sqlalchemy.orm import Session
from ..database import get_db
from .. import database, schemas, models, utils, oauth2

router = APIRouter(
    tags=["Auth"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut) # Changes default status code
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), ):
    
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Email already exists")
    user.password = utils.hash(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login", response_model=schemas.Token, status_code=status.HTTP_200_OK)
def login(user_credentials: OAuth2PasswordRequestForm = Depends() , db: Session = Depends(database.get_db)):
    # user_credentials: OAuth2PasswordRequestForm = Depends() # Returns username and password 
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    if not utils.verify_credentials(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    access_token = oauth2.create_acces_token(data={"user_id": user.id, "privileged": user.privileged }) # Roles like admin can be added in this payload

    return {"access_token": access_token, "token_type": "bearer"}

