from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.callback.search_fabric import SearchAction, SearchCallback
from app.bot.fonts.button_font import BasketButtonFont, BaseButtonFont, StartButtonFont
from app.bot.callback.basket_fabric import BasketAction, BasketCallback
from app.core import load_config


settings = load_config()


order_keyboards = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            *[InlineKeyboardButton(
                text=BasketButtonFont.write_admin + f" {ind+1}",
                url=f"https://t.me/{el[1:]}",
                ) for ind, el in enumerate(settings.bot.admins_et)
            ]
        ],
        [
            InlineKeyboardButton(
                text=StartButtonFont.basket,
                callback_data=StartButtonFont.callback_basket
            )
        ],
        [
            InlineKeyboardButton(
                text=StartButtonFont.catalog,
                callback_data=StartButtonFont.callback_catalog
            )
        ],
    ]
)


async def create_peg_basket(
    len_products_list: int,
    product_id: int|None = None,
    page: int = 0,
    count: int = 1,
    max_count: int = 10) -> InlineKeyboardMarkup:
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
                        callback_data=BasketCallback(
                            action=BasketAction.paginate,
                            page=page-1
                    ).pack()
                ))

            if end_offset < len_products_list:
                buttons_row.append(
                    InlineKeyboardButton(
                        text=BaseButtonFont.right,
                        callback_data=BasketCallback(
                            action=BasketAction.paginate,
                            page=page+1
                    ).pack()
                ))

            if buttons_row:
                builder.row(*buttons_row)

        count_list = []
        if count > 1:
            count_list.append(
                InlineKeyboardButton(
                text=BasketButtonFont.minus,
                callback_data=BasketCallback(
                    action=BasketAction.minus,
                    product_id=product_id,
                    page=page,
                    count=count-1
                ).pack()
            ))

        if count < max_count:
            count_list.append(InlineKeyboardButton(
                text=BasketButtonFont.plus,
                callback_data=BasketCallback(
                    action=BasketAction.plus,
                    product_id=product_id,
                    page=page,
                    count=count+1
                ).pack()
            ))
        builder.row(*count_list)

        builder.row(
            InlineKeyboardButton(
                text=BaseButtonFont.reset,
                callback_data=BasketCallback(
                    action=BasketAction.reset,
                ).pack()
            )
        )

    builder.row(InlineKeyboardButton(
        text=BasketButtonFont.return_to_filters,
        callback_data=SearchCallback(
            action=SearchAction.filter,
            page=page
        ).pack()
    ))

    builder.row(InlineKeyboardButton(
        text=BasketButtonFont.return_to_home,
        callback_data=SearchCallback(
            action=SearchAction.home
        ).pack()
    ))

    if page == len_products_list - 1:
        builder.row(InlineKeyboardButton(
        text=BasketButtonFont.confirm_order,
        callback_data=BasketCallback(
            action=BasketAction.confirm,
        ).pack()
    ))

    return builder.as_markup()
