from datetime import datetime

from pydantic import BaseModel
    

class SPostCreate(BaseModel):
    content: str
    title: str | None = None



class SPostRead(SPostCreate):
    id: int
    created_at: datetime
    updated_at: datetime


class SPostPaginationRead(BaseModel):
    items: list[SPostRead]
    total: int
    page: int
    per_page: int
    has_next: bool
    has_prev: bool
