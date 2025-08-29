import os
from pathlib import Path

from aiogram.types.input_file import FSInputFile

from app.db import Products
from app.core import load_config
from app.disks import yandex_storage
from app.bot.fonts.message_font import SearchFont
from app.bot.utils.catalog import CatalogUtils


settings = load_config()

class SearchUtils():
    @classmethod
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


    @classmethod
    def get_photo_products_by_id(cls, photo: str|None):
        print(f"{photo=}")
        if photo is None:
            path = os.path.join(os.getcwd(), yandex_storage.static_path, "smoke_tree.jpg")

        else:
            yandex_storage.check_file_in_static_path(Path(photo).name)
            path = os.path.join(os.getcwd(), photo)

        return FSInputFile(path=path)
