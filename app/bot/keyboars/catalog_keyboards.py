from typing import Any, Literal
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.db import ProductsDAO
from app.bot.callback.catalog_fabric import CallbackProduct, Action
from app.bot.fonts.button_font import BaseButtonFont
from app.bot.utils.catalog import CatalogUtils


async def get_peg_filter(column_name: str, filter_data: dict[str, Any],
                         page: int = 0) -> InlineKeyboardMarkup:  # TODOs доделать клавиатуру

    def _check_value_in_data(text: Any) -> str:
        item: str|None = filter_data.get(column_name)
        is_selected = item == text
        correct_text = CatalogUtils.translate_bool(text)
        return f"✅ {correct_text}" if is_selected else str(correct_text)

    def _check_correctness_variable(data: list[Any]) -> Literal["str", "int", "float", "bool"]:
        item = data[0]
        if isinstance(item, bool):
            return "bool"
        elif isinstance(item, str):
            return "str"
        elif isinstance(item, int):
            return "int"
        elif isinstance(item, float):
            return "float"
        else:
            raise TypeError("variable is not correct type")


    def _create_correct_select_button(text: str,
                                      callback_type: Literal["str", "int", "float", "bool"],
                                      el: Any,
                                      page: int = 0) -> InlineKeyboardButton:
        button: InlineKeyboardButton
        if callback_type == "str":
            button = InlineKeyboardButton(
                text=text,
                callback_data=CallbackProduct(
                    action=Action.select,
                    filter_type=column_name,
                    value_str=el,
                    page=page
                    ).pack()
            )
        elif callback_type == "int":
            button = InlineKeyboardButton(
                text=text,
                callback_data=CallbackProduct(
                    action=Action.select,
                    filter_type=column_name,
                    value_int=el,
                    page=page
                    ).pack()
            )
        elif callback_type == "float":
            button = InlineKeyboardButton(
                text=text,
                callback_data=CallbackProduct(
                    action=Action.select,
                    filter_type=column_name,
                    value_float=el,
                    page=page
                    ).pack()
            )
        elif callback_type == "bool":
            button = InlineKeyboardButton(
                text=text,
                callback_data=CallbackProduct(
                    action=Action.select,
                    filter_type=column_name,
                    value_bool=el,
                    page=page
                    ).pack()
            )
        else:
            raise TypeError("not correct type for inline button")
        return button

    builder = InlineKeyboardBuilder()

    data = await ProductsDAO.select_all_meaning_from_column(column_name)
    per_page = 5
    is_one_page = len(data) <= per_page

    if is_one_page:
        for el in data:
            builder.row(
                _create_correct_select_button(
                _check_value_in_data(el),
                _check_correctness_variable(data), # type: ignore
                el,
                page
            ))

    else:
        start_offset = page * per_page
        end_offset = start_offset + per_page
        one_page_data = data[start_offset: end_offset]

        for el in one_page_data:
            builder.row(
                _create_correct_select_button(
                _check_value_in_data(el),
                _check_correctness_variable(data), # type: ignore
                el,
                page
            ))

        buttons_row = []
        if page > 0:
            buttons_row.append(
                InlineKeyboardButton(
                    text=BaseButtonFont.left,
                    callback_data=CallbackProduct(
                        action=Action.paginate,
                        filter_type=column_name,
                        page=page-1
                ).pack()
            ))

        if end_offset < len(data):
            buttons_row.append(
                InlineKeyboardButton(
                    text=BaseButtonFont.right,
                    callback_data=CallbackProduct(
                        action=Action.paginate,
                        filter_type=column_name,
                        page=page+1
                ).pack()
            ))

        if buttons_row:
            builder.row(*buttons_row)

    builder.row(InlineKeyboardButton(
        text=BaseButtonFont.reset,
        callback_data=CallbackProduct(
            action=Action.reset,
            filter_type=column_name,
            page=page
        ).pack()
    ))

    builder.row(InlineKeyboardButton(
        text=BaseButtonFont.apply,
        callback_data=CallbackProduct(
            action=Action.apply
        ).pack()
    ))

    return builder.as_markup() # type: ignore