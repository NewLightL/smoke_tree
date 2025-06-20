
"""Base for class Query"""

from typing import Any

from sqlalchemy import delete, insert, select, update
from sqlalchemy.sql._typing import _ColumnsClauseArgument  # type: ignore

from app.db.helper import Helper, helper


class BaseDAO:
    model: _ColumnsClauseArgument[Any]
    conn: Helper = helper

    @classmethod
    async def select_all(cls, **filter_by: Any):
        async with cls.conn.sessionf() as sess:
            query = select(cls.model).filter_by(**filter_by)
            res = await sess.execute(query)
            return res.mappings().all()


    @classmethod
    async def select_one_or_none(cls, **filter_by: Any):
        async with cls.conn.sessionf() as sess:
            query = select(cls.model).filter_by(**filter_by)
            res = await sess.execute(query)
            return res.scalar_one_or_none()


    @classmethod
    async def select_by_id(cls, id_: int|str):
        async with cls.conn.sessionf() as sess:
            query = select(cls.model).filter_by(id=id_)
            res = await sess.execute(query)
            return res.scalar_one_or_none()


    @classmethod
    async def insert(cls, **data: Any):
        async with cls.conn.sessionf() as sess:
            query = insert(cls.model).values(**data).returning(cls.model)  # type: ignore
            await sess.execute(query)
            await sess.commit()
            return


    @classmethod
    async def delete(cls, **data: Any):
        async with cls.conn.sessionf() as sess:
            query = delete(cls.model).filter_by(**data)  # type: ignore
            await sess.execute(query)
            await sess.commit()


    @classmethod
    async def update_by_id(cls, id_: int, **kwargs: Any):
        async with cls.conn.sessionf() as sess:
            query = update(cls.model).values(**kwargs).filter_by(id=id_)  # type: ignore
            await sess.execute(query)
            await sess.commit()
