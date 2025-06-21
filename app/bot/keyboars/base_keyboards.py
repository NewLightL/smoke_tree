from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.fonts.button_font import StartButtonFont


start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=StartButtonFont.catalog,  # каталог
                              callback_data=StartButtonFont.callback_catalog)],
        [InlineKeyboardButton(text=StartButtonFont.channel,  # канал
                              url=StartButtonFont.callback_channel)]
    ]
)
