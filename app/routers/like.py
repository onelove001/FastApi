from fastapi import Response, status, HTTPException, Depends, APIRouter
from database import get_db
from ..schemas import *
from sqlalchemy.orm import Session
import models
from ..oauth import get_current_user


router = APIRouter(
    prefix = "/likes",
    tags = ["Like"]

)


@router.post("/", status_code=status.HTTP_201_CREATED)
def like(like: likeResponse, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post_obj = db.query(models.UserPost).filter(models.UserPost.id == like.post_id).first()

    if not post_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post of id {like.post_id} not found")

    like_query = db.query(models.Like).filter(models.Like.post_id == like.post_id, models.Like.user_id  == current_user.id)
    found_liked = like_query.first()
    if (like.dir == 1):
        if found_liked:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = f"User {current_user.id} already liked Post {like.post_id}")
        else:
            new_like = models.Like(post_id = like.post_id, user_id = current_user.id)
            db.add(new_like)
            db.commit()
            return {"Message": f"User {current_user.id} Successfully liked this post!"}
    else:
        if not found_liked:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"like object does not exist")
        else:
            like_query.delete(synchronize_session=False)
            db.commit()
            return {"Message": "Successfully unliked this post"}
    
