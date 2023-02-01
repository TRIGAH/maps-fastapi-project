from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class UserRequest(BaseModel):
    email : EmailStr
    password: str      

class UserResponse(BaseModel):    
    id : int
    email : EmailStr
    created_at: datetime

    class Config:
        orm_mode=True

class UserLoginRequest(BaseModel):
    email : EmailStr
    password: str   


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class PostRequest(Post):
    pass 

class PostRespone(Post):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode=True

class PostVotes(BaseModel):
    Post : PostRespone
    votes : int

    class Config:
        orm_mode=True
     


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id : Optional[str] = None


class Vote(BaseModel):
    post_id : int
    dir: conint(le=1)