from sqlalchemy import delete, exists, func, insert, literal, select
from sqlalchemy.exc import IntegrityError

from app.database.session import session
from app.models.post import Post, post_likes
from app.schemas.pagination import SPagination
from app.schemas.post import SPostCreate


class PostRepository:
    """
    Данный класс предназначен для работы с таблицей "posts" в БД.

    Методы:

    -get_posts: Используется для получения всех постов из БД.
                Принимает пагинационную схему и необязательный ID пользователя.
                Возвращает словарь, содержащий список объектов Post с динамическими
                полями likes_count и is_liked, а также необходимые флаги для
                определения наличия следующей/предыдущей страницы.

    -create_post: Используется для создания новой записи в таблице.
                  Принимает Pydantic-схему с данными поста и ID автора.
                  Возвращает созданный объект Post.

    -like_post: Реализует логику "переключателя" (toggle) лайка.
                Если лайк уже существует — удаляет его, если нет — создает.
                Принимает ID пользователя и ID поста. Возвращает обновленный
                объект Post с актуальными данными по лайкам для корректного
                отображения на фронтенде.
    """

    @classmethod
    async def get_posts(
        cls, pagination: SPagination, user_id: int | None
    ) -> dict:
        async with session() as new_session:
            likes_count_subquery = (
                select(func.count(post_likes.c.user_id))
                .where(post_likes.c.post_id == Post.id)
                .correlate(Post)
                .scalar_subquery()
            )
            if user_id:
                is_liked_subquery = select(
                    exists()
                    .where(
                        post_likes.c.post_id == Post.id,
                        post_likes.c.user_id == user_id,
                    )
                    .correlate(Post)
                ).scalar_subquery()
            else:
                is_liked_subquery = select(literal(False)).scalar_subquery()

            skip = (pagination.page - 1) * pagination.per_page
            query = (
                select(
                    Post,
                    likes_count_subquery.label("likes_count"),
                    is_liked_subquery.label("is_liked"),
                )
                .order_by(Post.created_at)
                .limit(pagination.per_page)
                .offset(skip)
            )
            result = await new_session.execute(query)
            posts_with_likes = []
            for row in result.all():
                post = row[0]
                post.likes_count = row[1]
                post.is_liked = row[2]
                posts_with_likes.append(post)
            total_query = select(func.count()).select_from(Post)
            total = await new_session.execute(total_query)
            total = total.scalar() or 0
            has_next = total > (pagination.page * pagination.per_page)
            has_prev = pagination.page > 1
            return {
                "items": posts_with_likes,
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

    @classmethod
    async def like_post(cls, user_id: int, post_id: int) -> Post | None:
        async with session() as new_session:
            stmt = insert(post_likes).values(user_id=user_id, post_id=post_id)
            try:
                await new_session.execute(stmt)
            except IntegrityError:
                await new_session.rollback()
                stmt = delete(post_likes).where(
                    post_likes.c.user_id == user_id,
                    post_likes.c.post_id == post_id,
                )
                await new_session.execute(stmt)
            likes_subquery = (
                select(func.count(post_likes.c.user_id))
                .where(post_likes.c.post_id == post_id)
                .scalar_subquery()
            )
            is_liked_subquery = select(
                exists().where(
                    post_likes.c.post_id == Post.id,
                    post_likes.c.user_id == user_id,
                )
            ).scalar_subquery()
            await new_session.commit()
            post_query = select(
                Post,
                likes_subquery.label("likes_count"),
                is_liked_subquery.label("is_liked"),
            ).where(Post.id == post_id)
            result = await new_session.execute(post_query)
            row = result.first()
            if row:
                post, count_val, is_liked = row
                post.likes_count = count_val
                post.is_liked = is_liked
                return post
