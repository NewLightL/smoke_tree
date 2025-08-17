from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.bot.fonts.message_font import MessageFont
from app.bot.keyboars.base_keyboards import start_keyboard
from aiogram.fsm.state import default_state


router = Router()


@router.message(CommandStart())
async def start_message(mess: Message, state: FSMContext):
    await state.set_state(default_state)
    await state.clear()
    await mess.answer(MessageFont.start, reply_markup=start_keyboard)
