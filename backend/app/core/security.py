from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher


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
