from typing import Any

from sqlalchemy import JSON, ARRAY, String
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, declared_attr
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    type_annotation_map = {
        dict[str, Any]: JSON,
        list[str]: ARRAY(String)
    }

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:  # type: ignore
        return f"{cls.__name__}".lower()

    def __repr__(self) -> str:
        return f'{self.__tablename__} '
