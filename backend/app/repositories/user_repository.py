from typing import Sequence

from sqlalchemy import select

from app.database.session import session
from app.models.user import User
from app.schemas.user import SUserCreate


class UserRepository:
    """
    Данный класс предназначен для работы с таблицей "users" в БД.

    Методы:

    -add_one: Используется для создания записи о пользователе в БД.
              Внутри содержит метод для хэширования пароля.
              Возвращает id созданного пользователя.

    -get_by_username: Используется для поиска пользователя
                      по его username полю и возвращает объект
                      пользователя или None.
    
    -get_by_id: Используется для поиска пользователя
                по его id полю и возвращает объект пользователя
                или None.
    """
    @classmethod
    async def add_one(cls, data: SUserCreate) -> User:
        async with session() as new_session:
            user_dict = data.model_dump()
            user_dict["password"] = user_dict.pop("password").get_secret_value()
            user = User(**user_dict)
            new_session.add(user)
            await new_session.commit()
            return user

    @classmethod
    async def get_by_username(cls, username: str) -> User | None:
        async with session() as new_session:
            query = select(User).where(User.username == username)
            result = await new_session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_by_id(cls, id: int) -> User | None:
        async with session() as new_session:
            query = select(User).where(User.id == id)
            result = await new_session.execute(query)
            user_model = result.scalar_one_or_none()
            return user_model

    @classmethod
    async def get_users(cls) -> Sequence[User]:
        async with session() as new_session:
            query = select(User)
            result = await new_session.execute(query)
            user_models = result.scalars().all()
            return user_models
    

