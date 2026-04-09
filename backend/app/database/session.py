from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import settings
from app.models.base import Base
from app.models.user import User
from app.models.post import Post, Comment, post_likes


engine = create_async_engine(
    settings.get_db_url()
)

session = async_sessionmaker(engine, expire_on_commit=False)
