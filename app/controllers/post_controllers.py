from sqlalchemy.orm import Session

from app.config import config
from app.models.post import Post
from app.models.user import User
from app.schemas.post import PostCreate
import redis
import jwt


redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)


def add_post(db: Session, post: PostCreate, token: str):
    payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
    user = db.query(User).filter(User.email == payload.get("sub")).first()
    if not user:
        return None
    new_post = Post(text=post.text, user_id=user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def get_posts(db: Session, token: str):
    payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
    user = db.query(User).filter(User.email == payload.get("sub")).first()
    if not user:
        return None

    cache_key = f"posts:{user.id}"
    cached_posts = redis_client.get(cache_key)
    if cached_posts:
        return cached_posts

    posts = db.query(Post).filter(Post.user_id == user.id).all()
    redis_client.setex(cache_key, 300, str(posts))
    return posts


def delete_post(db: Session, post_id: int, token: str):
    payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
    user = db.query(User).filter(User.email == payload.get("sub")).first()
    if not user:
        return None

    post = db.query(Post).filter(Post.id == post_id, Post.user_id == user.id).first()
    if not post:
        return None

    db.delete(post)
    db.commit()
    redis_client.delete(f"posts:{user.id}")
    return True
