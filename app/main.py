from fastapi import FastAPI
from routers import auth_routers, post_routers

from database import Base, engine


def create_app():
    app = FastAPI()

    Base.metadata.create_all(bind=engine)

    app.include_router(auth_routers.router, prefix="/auth", tags=["Authentication"])
    app.include_router(post_routers.router, prefix="/posts", tags=["Posts"])

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)