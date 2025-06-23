from sqlalchemy import select

from app.db.basedao import BaseDAO
from app.db.layout import Products


class ProductsDAO(BaseDAO):
    model = Products

    @classmethod
    async def select_all_meaning_from_column(cls, column_name: str):
        column = getattr(cls.model, column_name)
        query = select(column).distinct().order_by(column)

        async with cls.conn.sessionf() as sess:
            res = await sess.execute(query)
            return res.scalars().all()