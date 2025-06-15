from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery


router = Router()


@router.message(CommandStart())
async def start_message(mess: Message):
    await mess.answer(f"Привет, {mess.from_user.full_name}")
