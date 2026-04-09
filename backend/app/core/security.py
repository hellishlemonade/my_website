from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher

from app.core.config import settings


password_hash = PasswordHash((BcryptHasher(),))


def hash_pwd(password: str) -> str:
    """
    Хэширование пароля с помощью переданных алгоритмов хэширования.
    """
    return password_hash.hash(password)


def verify_pwd(password: str, hashed_password: str) -> tuple[bool, str | None]:
    """
    Проверка введенного пароля и возврат в формате [bool, str | None].

    Если предоставленный хэш является устаревшим,
    то дополнительно возвращается строка с новым хэшем.
    """
    return password_hash.verify_and_update(password, hashed_password)


def create_access_token(data: dict) -> str:
    """
    Создает зашифрованный JWT токен.
    data: словарь с данными (например, {"sub": user_id})
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict | None:
    """
    Расшифровывает токен и проверяет его валидность.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.PyJWTError:
        return None
