from app.bot.fonts.message_font import BasketFont
from app.db import Products, ProductsDAO


class BasketUtils:
    @classmethod
    async def get_card_basket(cls, basket: dict[int, int]):
        ids = list(basket.keys())

        products_basket: list[Products] = await ProductsDAO.get_all_by_id(ids)
        products_text = ""
        total_cost = 0

        for el in products_basket:
            name = el.name
            count = basket[el.id]
            total_cost += el.price * count

            products_text += f"{name} - {count}шт\n"

        return BasketFont.card_basket.format(products_text, total_cost)