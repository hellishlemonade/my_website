from sqlalchemy import func, select

from app.database.session import session
from app.models.post import Post
from app.schemas.pagination import SPagination
from app.schemas.post import SPostCreate


class PostRepository:
    """
    Данный класс предназначен для работы с таблицей "posts" в БД.

    Методы:

    -get_posts: Используется для получения всех постов из БД.
                Принимает пагинационную схему и возвращает словарь,
                содержащий список постов и необходимые флаги для
                оперделения наличия следующей/предыдущей страницы.

    -create_post: Используется для создания поста ...
    """

    @classmethod
    async def get_posts(cls, pagination: SPagination) -> dict:
        async with session() as new_session:
            count_query = select(func.count()).select_from(Post)
            total_result = await new_session.execute(count_query)
            total = total_result.scalar() or 0
            skip = (pagination.page - 1) * pagination.per_page
            query = (
                select(Post)
                .order_by(Post.created_at)
                .limit(pagination.per_page)
                .offset(skip)
            )
            result = await new_session.execute(query)
            posts = result.scalars().all()
            has_next = total > (pagination.page * pagination.per_page)
            has_prev = pagination.page > 1
            return {
                "items": posts,
                "total": total,
                "page": pagination.page,
                "per_page": pagination.per_page,
                "has_next": has_next,
                "has_prev": has_prev,
            }

    @classmethod
    async def create_post(cls, data: SPostCreate, author_id: int) -> Post:
        async with session() as new_session:
            post_dict = data.model_dump()
            post = Post(**post_dict, author_id=author_id)
            new_session.add(post)
            await new_session.commit()
            return post
