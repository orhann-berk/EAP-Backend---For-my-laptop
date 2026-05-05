from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.database import get_db
from database import models
from database.hash import Hash
from auth.oauth2 import create_access_token
import re

router = APIRouter(prefix="/register", tags=["registration"])


class RegisterRequest(BaseModel):
    email: str
    password: str


def is_valid_email(email):
    if " " in email:
        return False

    pattern = r"^[^@ ]+@[^@ ]+\.[^@ ]+$"
    return re.match(pattern, email) is not None


def send_confirmation_email(email):
    print("Confirmation email sent to " + email)


@router.post("", status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    if not is_valid_email(request.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please enter a valid email address",
        )

    if len(request.password) < 12:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 12 characters",
        )

    user = db.query(models.User).filter(models.User.email == request.email).first()

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered",
        )

    new_user = models.User(
        email=request.email.lower(),
        hashed_password=Hash.hash_password(request.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    send_confirmation_email(request.email)

    access_token = create_access_token(data={"sub": request.email})

    return {
        "message": "User registered successfully",
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": new_user.id,
        "email": request.email,
        "redirect_url": "/login",
    }
