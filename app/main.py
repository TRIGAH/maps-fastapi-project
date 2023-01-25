from typing import Optional,List
from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from random import randrange
from . import models,utils
from .database import engine,get_db
from sqlalchemy.orm import session
from .schemas import PostRequest,PostRespone,UserRequest,UserResponse
from .routers import post,user,auth


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


my_posts=[{"title":"My Year of Milking","content":"I will milk it","id":1},{"title":"ON GOD","content":"Only God can say NO","id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_post_index(id):
    for i,p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Welcome to My API"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)





#User Endpoints



            