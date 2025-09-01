from app.bot.fonts.message_font import BasketFont, SearchFont
from app.bot.utils.catalog import CatalogUtils
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
            taste = el.taste
            brand = el.brand
            count = basket[el.id]
            total_cost += el.price * count

            products_text += f"{brand} {name}, {taste} - {count}шт\n"

        return BasketFont.card_basket.format(products_text, total_cost)

    @classmethod
    def get_card_products_in_basket(cls, product: Products|None, count: int = 1):
        if product is None:
            text = BasketFont.basket_is_empty
        else:
            text = BasketFont.card_products_in_basket.format(
                product.name,
                product.brand,
                product.taste,
                product.volume,
                product.fortress,
                product.type_nicotine,
                CatalogUtils.translate_bool(product.chill),
                (SearchFont.last_products if
                 product.amount <= 3 else
                 SearchFont.more_products),
                product.amount,
                product.price,
                count)

        return text
