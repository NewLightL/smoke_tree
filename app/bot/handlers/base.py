from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.bot.fonts.message_font import MessageFont
from app.bot.keyboars.base_keyboards import start_keyboard


router = Router()


@router.message(CommandStart())
async def start_message(mess: Message, state: FSMContext):
    await state.clear()
    await mess.answer(MessageFont.start, reply_markup=start_keyboard)
