from fastapi import FastAPI

from app import routers
from app.database import Base, engine


def create_app():
    app = FastAPI()

    Base.metadata.create_all(bind=engine)

    app.include_router(routers.auth_routers.router, prefix="/auth", tags=["Authentication"])
    app.include_router(routers.post_routers.router, prefix="/posts", tags=["Posts"])

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)