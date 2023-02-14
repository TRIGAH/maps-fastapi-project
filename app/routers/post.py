from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import models,oauth2
from ..database import engine,get_db
from sqlalchemy.orm import session
from ..schemas import PostRequest,PostRespone,PostVotes
from typing import List,Optional
from sqlalchemy import func
router = APIRouter(tags=["Posts"])

@router.get("/posts",response_model=List[PostVotes])
def get_posts(db: session  = Depends(get_db), current_user : int = Depends(oauth2.get_current_user),limit : int =2 ,skip : int =2, search : Optional[str]=""):
    # cursor.execute(""" SELECT * FROM posts """)

    posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes"))\
    .join(models.Vote,models.Vote.post_id == models.Post.id, isouter=True)\
    .group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.post("/posts",status_code=status.HTTP_201_CREATED,response_model=PostRespone)
def create_posts(post: PostRequest, db: session  = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """ ,(post.title,post.content,post.published))

    new_post=models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post     

@router.get("/posts/{id}",response_model=PostVotes)
def get_post(id: int, response: Response, db: session  = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)): 
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes"))\
    .join(models.Vote,models.Vote.post_id == models.Post.id, isouter=True)\
    .group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")  

    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")  
                 
    return post


@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)    
def delete_post(id: int,db: session  = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")    

    post_query.delete(synchronize_session = False)
    db.commit()


@router.put("/posts/{id}",response_model=PostRespone)
def update_post(id: int, post: PostRequest, db: session  = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title,post.content,post.published,str(id),))
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")

    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")      

    post_query.update(post.dict(), synchronize_session=False)    
    db.commit()
    return post_query.first()