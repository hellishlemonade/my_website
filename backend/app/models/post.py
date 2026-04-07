from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Text

from app.models.user import User
from models.base import Base


class BaseContent(Base):
    __abstract__ = True

    content: Mapped[str] = mapped_column(Text)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )


class Post(BaseContent):
    __tablename__ = "posts"

    title: Mapped[Optional[str]] = mapped_column(String(50))

    author: Mapped["User"] = relationship(back_populates="posts", uselist=False)
