import inspect, os, sys

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from app import models
from sqlalchemy.orm import Session





appp = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    is_published: bool = True



while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'fastapidb', user='postgres', 
        password='olatunde8483', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection Succss!")
        break
    except Exception as err:
        print(f"Database Connection Failed With Error: {err}")
        time.sleep(3)


@appp.post("/sqlalchemy")
def create_user(db: Session = Depends(get_db)):
    return {"message": "success"}
    

@appp.get("/posts")
async def get_all_posts():
    cursor.execute("SELECT * FROM post")
    posts = cursor.fetchall()
    return {"data": posts}


@appp.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(new_post: Post):
    cursor.execute("INSERT INTO post (title, content, is_published) VALUES (%s, %s, %s) RETURNING * ", (new_post.title, new_post.content, new_post.is_published))
    post = cursor.fetchone()
    conn.commit()
    return {"data": post}


@appp.get("/posts/{id}")
async def get_post(id: int):
    cursor.execute("SELECT * FROM post WHERE id = %s", (str(id),) )
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist!")
    return {"data": post}


@appp.put("/posts/{id}")
async def update_post(id: int, post: Post):
    cursor.execute("UPDATE post SET title=%s, content=%s, is_published=%s WHERE id = %s returning *", (post.title, post.content, post.is_published, str(idm)))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post with the id: {id} does not exist!")
    return {"data":post}


@appp.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cursor.execute("DELETE FROM post WHERE id = %s RETURNING *", (str(id),))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post with the id: {id} does not exist!")
    return Response(status_code = status.HTTP_204_NO_CONTENT)


