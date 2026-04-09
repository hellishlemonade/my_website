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
                      по его username полюи возвращает объект
                      пользователя или None. 
    """
    @classmethod
    async def add_one(cls, data: SUserCreate) -> int:
        async with session() as new_session:
            user_dict = data.model_dump()
            user_dict["password"] = user_dict.pop("password").get_secret_value()
            user = User(**user_dict)
            new_session.add(user)
            await new_session.commit()
            return user.id

    @classmethod
    async def get_by_username(cls, username: str) -> User | None:
        async with session() as new_session:
            query = select(User).where(User.username == username)
            result = await new_session.execute(query)
            return result.scalar_one_or_none()
