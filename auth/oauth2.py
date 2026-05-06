from fastapi.params import Depends
from sqlalchemy.orm import Session
from database.database import get_db
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional, Annotated
from datetime import datetime, timedelta
from jose import jwt, JWTError
from database import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise credentials_exception

        user = (
            db.query(models.DbEmployee).filter(models.DbEmployee.email == email).first()
        )

        if user is None:
            raise credentials_exception

        return user

    except JWTError:
        raise credentials_exception
