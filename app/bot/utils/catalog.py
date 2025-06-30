from typing import Any

from app.bot.callback.catalog_fabric import CallbackProduct


class CatalogUtils:
    @classmethod
    def get_correct_variable(cls, callback_data_packed: str):
        unpack_callback_data = CallbackProduct.unpack(callback_data_packed)

        for key, el in unpack_callback_data:
            if el is not None and key.startswith("value"):
                return key, el
        raise TypeError("not correct callback data")

    @classmethod
    def translate_bool(cls, text: Any):
        correct_text: Any = text
        if isinstance(text, bool):
            if text == False:
                correct_text = "Нет"
            else:
                correct_text = "Да"

        if text in ("Да", "Нет"):
            if text == "Да":
                correct_text = True
            else:
                correct_text = False
        return correct_text
