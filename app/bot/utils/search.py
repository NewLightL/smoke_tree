import os
from typing import Any

from aiogram.types.input_file import FSInputFile

from app.db import Products
from app.core import load_config
from app.bot.fonts.message_font import SearchFont
from app.bot.utils.catalog import CatalogUtils


settings = load_config()

class SearchUtils():
    @classmethod  # TODOS доделать вывод сообщения
    def create_message_for_item_card(cls, product: Products|None):
        if product is None:
            text = SearchFont.incorrect_name
        else:
            text = SearchFont.card_item.format(
                product.name,
                product.brand,
                product.taste,
                product.volume,
                product.type_nicotine,
                CatalogUtils.translate_bool(product.chill),
                product.price)
        return text


    @classmethod  # TODOs доделать вывод фото
    def get_photo_products_by_id(cls, photo_id: int|None):
        # path = f"../../static/{photo_id}.jpg"
        if photo_id is None:
            return None
        path = os.path.join(os.getcwd(), settings.core.static_path, "photo",
                            "products", f'{photo_id}.jpg')
        return FSInputFile(path=path)
