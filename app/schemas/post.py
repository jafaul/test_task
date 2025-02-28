from pydantic import BaseModel, constr


class PostCreate(BaseModel):
    text: constr(max_length=1048576)  # 1MB limit


class PostResponse(BaseModel):
    id: int
    text: str
