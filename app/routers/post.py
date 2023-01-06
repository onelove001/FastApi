from sqlalchemy.orm import Session
from schemas import *
from sqlalchemy import func
from oauth import get_current_user
import models
from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from database import get_db

router = APIRouter(
    prefix = "/posts",
    tags = ["Posts"]
)

# ======== +++++++++ POSTS PATH OPERATIONS ======== ++++++++

# @router.get("/")
@router.get("/", response_model=List[PostLike])         
async def get_all_posts(db: Session = Depends(get_db), current_user: int = Depends(get_current_user), limit: int = 5, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.UserPost, func.count(models.Like.post_id).label("likes")).join(models.Like, models.Like.post_id == models.UserPost.id, isouter=True).group_by(models.UserPost.id).filter(models.UserPost.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    new_post = models.UserPost(user_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=PostLike )
async def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post = db.query(models.UserPost, func.count(models.Like.post_id).label("likes")).join(models.Like, models.Like.post_id == models.UserPost.id, isouter=True).group_by(models.UserPost.id).filter(models.UserPost.id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist!")
    return post                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   


@router.put("/{id}", response_model=PostResponse)
async def update_post(post: PostCreate, id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post_id = db.query(models.UserPost).filter(models.UserPost.id == id)
    if post_id.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist!")
    elif post_id.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You are not authorized to perform the requested action   ")
    else:
        post_id.update(post.dict(), synchronize_session = False)
        db.commit()
    return post_id.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post = db.query(models.UserPost).filter(models.UserPost.id == id)
    if post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist!")
    elif post.first().user_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = f"You are not authorized to perform the requested action!")
    else:
        post.delete(synchronize_session = False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
