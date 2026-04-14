from datetime import datetime

from pydantic import BaseModel
    

class SPostCreate(BaseModel):
    content: str
    title: str | None = None



class SPostRead(SPostCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    likes_count: int = 0
    is_liked: bool = False


class SPostPaginationRead(BaseModel):
    items: list[SPostRead]
    total: int
    page: int
    per_page: int
    has_next: bool
    has_prev: bool


class SCommentCreate(BaseModel):
    content: str


class SCommentRead(BaseModel):
    post_id: int
    author_id: int
    content: str
    created_at: datetime
    updated_at: datetime
