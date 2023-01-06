from sqlalchemy.orm import Session
from ..schemas import *
import models
from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from database import get_db
from utils import hash
from oauth import get_current_user

router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)
# ========+++++++++ USERS PATH OPERATIONS ========++++++++

@router.get("/", response_model = List[UserResponse])
async def get_all_user(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user.password = hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model = UserResponse)
async def get_user(id: int, db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist!")
    return user       