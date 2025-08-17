from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.fonts.button_font import (
    StartButtonFont, CatalogButtonFont,
    FiltersButtonFont, BaseButtonFont
    )


reset_search = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=BaseButtonFont.reset,
                              callback_data=BaseButtonFont.callback_reset)]
    ]
)


url_to_channel = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text=StartButtonFont.channel,
                             url=StartButtonFont.callback_channel)
    ]]
)


start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=StartButtonFont.catalog,  # каталог
                              callback_data=StartButtonFont.callback_catalog)],
        [InlineKeyboardButton(text=StartButtonFont.basket,  # корзина
                              callback_data=StartButtonFont.callback_basket)],
        [InlineKeyboardButton(text=StartButtonFont.channel,  # канал
                              url=StartButtonFont.callback_channel)]
    ]
)


search_catalog = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=CatalogButtonFont.filter,  # фильтр
                              callback_data=CatalogButtonFont.callback_filter)],
        [InlineKeyboardButton(text=CatalogButtonFont.search_by_name,  # поиск по названию
                              callback_data=CatalogButtonFont.callback_search_by_name)],
        [InlineKeyboardButton(text=CatalogButtonFont.search,  # поиск
                              callback_data=CatalogButtonFont.callback_search)],
    ]
)


all_filters = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=FiltersButtonFont.brand,  # бренд
                              callback_data=FiltersButtonFont.callback_brand),
        InlineKeyboardButton(text=FiltersButtonFont.taste,  # вкус
                              callback_data=FiltersButtonFont.callback_taste)],
        [InlineKeyboardButton(text=FiltersButtonFont.volume,  # объем
                              callback_data=FiltersButtonFont.callback_volume),
        InlineKeyboardButton(text=FiltersButtonFont.fortress,  # крепость
                              callback_data=FiltersButtonFont.callback_fortress)],
        [InlineKeyboardButton(text=FiltersButtonFont.chill,  # холодок
                              callback_data=FiltersButtonFont.callback_chill),
        InlineKeyboardButton(text=FiltersButtonFont.type_nicotine,  # тип никотина
                              callback_data=FiltersButtonFont.callback_type_nicotine)],
        [InlineKeyboardButton(text=FiltersButtonFont.price,  # цена
                              callback_data=FiltersButtonFont.callback_price)],
        [InlineKeyboardButton(text=BaseButtonFont.reset,  # сбросить
                              callback_data=BaseButtonFont.callback_reset)],
        [InlineKeyboardButton(text=BaseButtonFont.apply,  # применить
                              callback_data=BaseButtonFont.callback_apply)],
    ]
)
