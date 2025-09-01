from typing import Any, Sequence
from sqlalchemy import select, func

from app.db.basedao import BaseDAO
from app.db.layout import Products


class ProductsDAO(BaseDAO):
    model = Products

    @classmethod
    async def select_products_by_filter(cls, **filter_by: Any):  # type: ignore
        price_in_filter = "price" in filter_by.keys()
        basket_in_filter = "basket" in filter_by.keys()

        if basket_in_filter:
            del filter_by["basket"]

        async with cls.conn.sessionf() as sess:
            if not filter_by:
                query = select(Products)
            elif price_in_filter:
                standart_filter = filter_by.copy()
                del standart_filter['price']

                query = select(Products).filter(
                    Products.price <= int(filter_by["price"]), **standart_filter)
            else:
                query = select(Products).filter_by(**filter_by)

            query = query.filter(Products.amount > 0)
            res = await sess.execute(query)
            answer = res.scalars().all()
            if not answer:
                return None
            return answer


    @classmethod
    async def select_all_meaning_from_column(cls, column_name: str):
        column = getattr(cls.model, column_name)
        query = (select(column)
                .distinct()
                .order_by(column)
                .where(cls.model.amount > 0))

        async with cls.conn.sessionf() as sess:
            res = await sess.execute(query)
            return res.scalars().all()


    @classmethod  # TODOs сделать поиск по названию
    async def get_all_by_name(cls, name: str) -> Sequence[Products]:
        query = select(cls.model).where(
        Products.name.ilike(f"%{name}%"),
        Products.amount > 0
    ).order_by(
        func.similarity(Products.name, name).desc()
    )

        async with cls.conn.sessionf() as sess:
            res = await sess.execute(query)
            return res.scalars().all()


    @classmethod
    async def get_all_by_id(cls, ids_list: list[int]):
        stmt = (select(Products)
               .where(
                   Products.id.in_(ids_list)
                ))
        async with cls.conn.sessionf() as sess:
            result = await sess.execute(stmt)
            products = result.scalars().all()
            return products if products else None
