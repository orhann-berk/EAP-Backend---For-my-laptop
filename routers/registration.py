from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.database import get_db
from database import models
from database.hash import Hash
from datetime import datetime
import re

router = APIRouter(prefix="/register", tags=["registration"])


class RegisterRequest(BaseModel):
    fullName: str
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
    if not request.fullName:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Full name is required",
        )

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

    employee = (
        db.query(models.DbEmployee)
        .filter(models.DbEmployee.email == request.email.lower())
        .first()
    )

    if employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered",
        )

    new_employee = models.DbEmployee(
        fullName=request.fullName,
        email=request.email.lower(),
        password=Hash.hash_password(request.password),
        creationTimestamp=datetime.now(),
        updatedTimestamp=datetime.now(),
        isActive=True,
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    send_confirmation_email(new_employee.email)

    return {
        "message": "User registered successfully",
        "redirect_url": "/login",
    }
