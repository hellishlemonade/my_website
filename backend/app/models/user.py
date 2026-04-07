from enum import Enum
from typing import Optional

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.post import Comment, Post
from app.models.base import Base


class UserRole(Enum):
    """
    Enum для добавления статусов пользователей
    """

    ADMIN = "admin"
    CUSTOMER = "customer"


class User(Base):
    __tablename__ = "users"

    first_name: Mapped[Optional[str]] = mapped_column(String(30))
    last_name: Mapped[Optional[str]] = mapped_column(String(30))
    username: Mapped[str] = mapped_column(String(20), unique=True)
    _password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole, name="user_role_enum", native_enum=False),
        default=UserRole.CUSTOMER,
        nullable=True,
    )

    posts: Mapped[list["Post"]] = relationship(
        back_populates="author", uselist=True
    )
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="author", uselist=True
    )

    def set_password(self, password):
        pass

    def verify_password(self, password):
        pass

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
