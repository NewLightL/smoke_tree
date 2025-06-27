from typing import Any
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.db import ProductsDAO
from app.bot.callback.catalog_fabric import CallbackProduct, Action
from app.bot.fonts.button_font import BaseButtonFont


async def get_peg_filter(column_name: str, filter_data: dict[str, Any],
                         page: int = 0) -> InlineKeyboardMarkup:  # TODOs доделать клавиатуру

    def _check_value_in_data(text: Any):
        item: str|None = filter_data.get(column_name)
        # if isinstance(item, bool):
        #     correct_text = str(int(text))
        # else:
        # is_selected=False, correct_text='False',

        #! type(correct_text)=<class 'str'>,
        #! text=False, type(text)=<class 'bool'>,
        #! item='1', type(item)=<class 'str'>,
        #! filter_data={'brand': 'Husky', 'volume': '35.0', 'chill': '1'}
        #! is_selected=False, correct_text='True',
        #! type(correct_text)=<class 'str'>, text=True,
        #! type(text)=<class 'bool'>, item='1', type(item)=<class 'str'>,
        #! filter_data={'brand': 'Husky', 'volume': '35.0', 'chill': '1'}

        correct_text = str(text)
        is_selected = item == correct_text
        # print(f"{is_selected=}, {correct_text=}, {type(correct_text)=}, "\
        #     f"{text=}, {type(text)=}, {item=}, {type(item)=}, {filter_data=}")
        return f"✅ {text}" if is_selected else str(text)

    builder = InlineKeyboardBuilder()

    data = await ProductsDAO.select_all_meaning_from_column(column_name)
    per_page = 5
    is_one_page = len(data) <= per_page

    if is_one_page:
        for el in data:
            builder.row(
                InlineKeyboardButton(
                    text=_check_value_in_data(el),
                    callback_data=CallbackProduct(
                        action=Action.select,
                        filter_type=column_name,
                        value=el,
                        page=page
                    ).pack()
                ))

    else:
        start_offset = page * per_page
        end_offset = start_offset + per_page
        one_page_data = data[start_offset: end_offset]

        for el in one_page_data:
            builder.row(InlineKeyboardButton(
                text=_check_value_in_data(el),
                callback_data=CallbackProduct(
                    action=Action.select,
                    filter_type=column_name,
                    value=el,
                    page=page).pack())
            )

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