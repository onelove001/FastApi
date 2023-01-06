from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True


class PostCreate(PostBase):
    pass


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created: datetime

    class Config:
        orm_mode = True
        

class PostResponse(PostBase):
    id: int
    created: datetime
    user_id: int
    user: UserResponse

    class Config:
        orm_mode = True


class PostLike(BaseModel):
    UserPost: PostResponse   
    likes: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass


class UserLogin(BaseModel):
    email: EmailStr
    password: str



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class likeResponse(BaseModel):
    post_id: int
    dir: conint(le=1)









