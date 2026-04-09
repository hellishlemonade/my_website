import re
from typing import Annotated, Optional

from pydantic import AfterValidator, BaseModel, Field, SecretStr

from app.models.user import UserRole


def check_password_strength(v: SecretStr) -> SecretStr:
    pw = v.get_secret_value()
    pattern = r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_=])[A-Za-z\d@$!%*?&].*$"
    if not re.match(pattern, pw):
        raise ValueError("Пароль слишком слабый: нужны заглавная буква, цифра и спецсимвол")
    return v

StrongPassword = Annotated[
    SecretStr, 
    Field(min_length=8, max_length=72), 
    AfterValidator(check_password_strength)
]


class SUserCreate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: str = Field(min_length=3, max_length=20)
    password: StrongPassword
    role: UserRole = UserRole.CUSTOMER


class SUserToken(BaseModel):
    access_token: str
    token_type: str
