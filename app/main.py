import inspect, os, sys


current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)   
sys.path.insert(0, parent_dir)

from fastapi import FastAPI
import models
from app.database import engine
from app.config import settings
from app.routers import user, post, authentication, like

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def dashboard():
    return {"Welcome": "Fast Api Routes"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(like.router)




