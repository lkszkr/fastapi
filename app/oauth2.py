from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import database, models
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

from app import schemas

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_acces_token(data: dict):
    to_encode = data.copy() # Coping dictionary to the new variable
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # Token expire time
    to_encode.update({"exp": expire })  # Adding expire time
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # Creating token
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = str(payload.get("user_id"))
        privileged: bool = bool(payload.get("privileged"))
        # Not working properly
        #print(type(payload.get("user_id")))
        #id: str = payload.get("user_id")
        if id is None or privileged is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id, privileged=privileged)
    except JWTError:
        raise credentials_exception
    return token_data

# Used to protect routes, it calls verify_access_token and returns data from token (ex. id, user privileges) that can be accesed and used when dependencies are added in routes
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not verify", headers={"WWW-Authenticate": "Bearer"})
    
    token_user_data = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token_user_data.id).first()
    return user

