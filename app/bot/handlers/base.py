from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from app.bot.fonts.message_font import MessageFont
from app.bot.keyboars.base_keyboards import start_keyboard

router = Router()


@router.message(CommandStart())
async def start_message(mess: Message):
    await mess.answer(MessageFont.start, reply_markup=start_keyboard)
