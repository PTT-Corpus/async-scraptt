from pydantic import BaseModel


class PostComment(BaseModel):
    type: str | None
    author: str | None
    content: str | None
    order: int


class Post(BaseModel):
    id: str
    board: str
    title: str
    author: str
    created_at: int
    content: str
    comment_reaction: dict[str, int]
    comments: list[PostComment]
