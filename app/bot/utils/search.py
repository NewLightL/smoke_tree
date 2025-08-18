import os

from aiogram.types.input_file import FSInputFile

from app.db import Products
from app.core import load_config
from app.bot.fonts.message_font import SearchFont
from app.bot.utils.catalog import CatalogUtils


settings = load_config()

class SearchUtils():
    @classmethod  # TODOS доделать вывод сообщения
    def create_message_for_item_card(cls, product: Products|None):
        if not product:
            text = SearchFont.incorrect_name
        else:
            text = SearchFont.card_item.format(
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
                product.price)
        return text


    @classmethod  # TODOs доделать вывод фото
    def get_photo_products_by_id(cls, photo: int|None):
        # path = f"../../static/{photo_id}.jpg"
        path = os.path.join(os.getcwd(), f'{photo}')
        if photo is None or not os.path.exists(path):
            path = os.path.join(os.getcwd(), settings.core.static_path, "photo/smoke_tree.jpg")
            return FSInputFile(path=path)
        return FSInputFile(path=path)
