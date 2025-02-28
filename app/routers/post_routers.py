from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from app.controllers.post_controllers import add_post, get_posts, delete_post
from app.schemas.post import PostCreate

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/")
def create_post(post: PostCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    new_post = add_post(db, post, token)
    if not new_post:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"postID": new_post.id}


@router.get("/")
def fetch_posts(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    posts = get_posts(db, token)
    if not posts:
        raise HTTPException(status_code=401, detail="Invalid token")
    return posts


@router.delete("/{post_id}")
def remove_post(post_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    if not delete_post(db, post_id, token):
        raise HTTPException(status_code=404, detail="Post not found or unauthorized")
    return {"message": "Post deleted successfully"}
