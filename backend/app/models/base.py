from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        attrs = [
            f"{column.name}={getattr(self, column.name)!r}"
            for column in self.__table__.columns
            if not isinstance(column.type, DateTime) and not column.foreign_keys
        ]
        return f"{class_name}({', '.join(attrs)})"
