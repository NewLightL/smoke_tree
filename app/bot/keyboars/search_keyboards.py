from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.callback.search_fabric import SearchCallback, SearchAction
from app.bot.fonts.button_font import BaseButtonFont, SearchButtonFont


async def get_search_peg_keyboard(
    len_products_list: int,
    product_id: int|None = None ,
    page: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    per_page = 1
    is_len_is_not_null = len_products_list != 0
    is_one_page = len_products_list == per_page

    if is_len_is_not_null:
        if not is_one_page:
            start_offset = page * per_page
            end_offset = start_offset + per_page

            buttons_row = []
            if page > 0:
                buttons_row.append(
                    InlineKeyboardButton(
                        text=BaseButtonFont.left,
                        callback_data=SearchCallback(
                            action=SearchAction.paginate,
                            page=page-1
                    ).pack()
                ))

            if end_offset < len_products_list:
                buttons_row.append(
                    InlineKeyboardButton(
                        text=BaseButtonFont.right,
                        callback_data=SearchCallback(
                            action=SearchAction.paginate,
                            page=page+1
                    ).pack()
                ))

            if buttons_row:
                builder.row(*buttons_row)
        builder.row(
            InlineKeyboardButton(
                text=SearchButtonFont.select_products,
                callback_data=SearchCallback(
                    action=SearchAction.select,
                    product_id=product_id,
                ).pack()
            )
        )

    builder.row(InlineKeyboardButton(
        text=SearchButtonFont.return_to_filters,
        callback_data=SearchCallback(
            action=SearchAction.filter,
            page=page
        ).pack()
    ))

    builder.row(InlineKeyboardButton(
        text=SearchButtonFont.return_to_home,
        callback_data=SearchCallback(
            action=SearchAction.home
        ).pack()
    ))

    builder.row(
        InlineKeyboardButton(
            text=SearchButtonFont.return_to_basket,
            callback_data=SearchCallback(
                action=SearchAction.basket,
            ).pack()
        )
    )

    return builder.as_markup() # type: ignore
